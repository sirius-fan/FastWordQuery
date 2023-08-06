# -*- coding:utf-8 -*-
import os
import re

from bs4 import Tag

from ..base import *
from datetime import datetime

souka_download_mp3 = True

@register([u'Souka 日语在线词典', u'Souka Japanese'])
class Souka(WebService):

    def __init__(self):
        super(Souka, self).__init__()

    def _get_url(self):
        return u'https://soukaapp.com/dict/{}'.format(self.quote_word)

    def _get_from_api(self):
        data = self.get_response(self._get_url())
        soup = parse_html(data)
        result = {
            'definition': u'', 
            'pronunciation': u'',
            'audio': u'', 
            'examples': u'',
        }

        # 发音
        tag = soup.find('div', class_='headword')
        if tag:
            pronunciation = tag.find('h5')
            if pronunciation:
                result['pronunciation'] = pronunciation.get_text()
                result['pronunciation'] = re.sub(r' 【.*】', '', result['pronunciation'])
            audio = tag.find('source')
            if audio:
                result['audio'] = audio.get('src')
            tag.decompose()
        
        # 释义
        tag = soup.find('div', class_='definition')
        if tag:
            result['definition'] = str(tag.find('p'))
            result['definition'] = re.sub(r'\n', '<br>', result['definition'])
            tag.decompose()
        
        # 例句
        tag = soup.find('div', class_='examples')
        if tag:
            result['examples'] = str(tag.find('ol'))
            tag.decompose()

        return self.cache_this(result)
    

    @export([u'释义', u'Definition'])
    def fld_definition(self):
        return self._get_field('definition')
    
    @export([u'发音', u'Pronunciation'])
    def fld_pronunciation(self):
        return self._get_field('pronunciation')
    
    @export([u'例句', u'Examples'])
    def fld_examples(self):
        return self._get_field('examples')
    
    @export([u'录音', u'Audio'])
    def fld_audio(self):
        audio_url = self._get_field('audio')
        if souka_download_mp3 and audio_url:
            filename = get_hex_name(self.unique.lower(), audio_url, 'mp3')
            if os.path.exists(filename) or self.download(audio_url, filename):
                return self.get_anki_label(filename, 'audio')
            else:
                return self.get_anki_label(audio_url, 'audio')
        else:
            return ''