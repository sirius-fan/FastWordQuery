# -*- coding:utf-8 -*-
import os
import re

from bs4 import Tag

from ..base import *
from datetime import datetime

dizionario_italiano_base_url = u'https://www.dizionario-italiano.it/dizionario-italiano.php?parola={}100'

@register([u'dizionario_italiano', u'Dizionario Italiano'])
class dizionarioItaliano(WebService):

    def __init__(self):
        super().__init__()

    def _get_url(self):
        return dizionario_italiano_base_url.format(self.quote_word)

    def _get_from_api(self):
        data = self.get_response(self._get_url())
        soup = parse_html(data)
        try:
            result = {'definizione': self.__get_defs(soup),
                      'sillabe': self.__get_sillabe(soup, self.word),
                      'lemma': self.__get_lemma(soup),
                      'pronuncia': self.__get_pronuncia(soup),
                      'grammatica': self.__get_grammatica(soup),
                      'soundlink': self.__get_sound_link(soup),
                      'url': self._get_url()}
        except Exception as e:
            print('exception is ', e)
            result = {'definizione': '',
                      'sillabe': '',
                      'lemma': "",
                      'pronuncia': '',
                      'grammatica': '',
                      'soundlink': '',
                      'url': ''}
        return self.cache_this(result)

    @export('IPA')
    def fld_IPA(self):
        seg = self._get_field('pronuncia')
        print(seg)
        return seg
    
    def __fld_mp3(self):
        audio_url = self._get_field('soundlink')
        if audio_url:
            filename = get_hex_name(self.unique.lower(), audio_url, 'mp3')
            if os.path.exists(filename) or self.net_download(filename, audio_url):
                return self.get_anki_label(filename, 'audio')
        return ''

    @export('Sound')
    def fld_mp3(self):
        return self.__fld_mp3()

    @export('Italian Definition')
    def fld_definition(self):
        try:
            return '\n'.join(self._get_field('definizione'))
        except Exception():
            return ""
    
    @export('Sillabe')
    def fld_sillabe(self):
        return str(self._get_field('sillabe'))

    @export('Grammatica') 
    def fld_grammatica(self):
        return ' '.join(self._get_field('grammatica'))

    def __get_lemma(self, soup):
        lemma = soup.find('span', class_='lemma')
        if lemma is not None:
            # Getting only span text + removing white spaces at the end
            return lemma.find(text=True, recursive=False).rstrip()

    def __get_sillabe(self, soup, word):
        lemma = soup.find(class_='lemma')
        small_list = lemma.find_all_next('small')
        for el in small_list:
            if el.parent not in lemma.children:
                try:
                    sillabe = el.span.find(text=True, recursive=False)
                except AttributeError:  # Word has no syllable division
                    return [word]
                break

        split_indexes = [pos for pos,
                         char in enumerate(sillabe) if char == "|"]
        # necessario perchè le sillabazioni contengono gli accenti di pronuncia
        tmp = list(word)
        for i in split_indexes:
            tmp = tmp[0:i] + ["|"] + tmp[i:]
            sillabe = ''.join(tmp).split("|")
        return sillabe

    def __get_pronuncia(self, soup):
        pronuncia = soup.find('span', class_="paradigma")
        return pronuncia.text[10:]

    def __get_grammatica(self, soup):
        gram = soup.find_all('span', class_="grammatica")
        return [x.text for x in gram]


    def __generate_current_date(self):
        today = datetime.now()
        date = str(today.year) + str(today.month) + str(today.day)
        time = str(today.hour) + str(today.minute) + str(today.second)
        dateTime = date + time
        return dateTime

    def __get_sound_link(self, soup):
        mp3_path = soup.find('span', class_="psPlay")['data-audio'].strip()
        sound_url = "https://www.dizionario-italiano.it/{0}&sc=1&d={1}".format(mp3_path, self.__generate_current_date())
        print('data_audio', sound_url)
        return sound_url

    def __get_locuzioni(self, soup):
        bad_loc = soup.find_all('span', class_='cit_ita_1')
        loc = [x.text for x in bad_loc]
        return loc

    def __get_defs(self, soup):
        defs = []
        for definitions in soup.find_all('span', class_='italiano'):
            children_content = ''
            for children in definitions.findChildren():
                if children.string is None:
                    continue
                try:
                    if children.attrs['class'][0] in ('esempi', 'autore'):
                        continue
                    else:
                        children_content += children.text
                        children_content += ' '
                        children.decompose()
                except KeyError:
                    continue
            if children_content != '':
                defs.append(
                    f"{children_content.upper()} -- {definitions.text.replace('()', '')}")
            else:
                defs.append(definitions.text)
        if len(defs) == 0:
            raise exceptions.WordNotFoundError()
        return defs
