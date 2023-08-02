# [dev] FastWordQuery_
**没改完，慢慢来**

适配pyqt6

适配anki新api

修改失效词典

修复css文件不能载入的问题（暂时有效）（  [问题来源](https://github.com/ankitects/anki/blob/main/ts/editor/plain-text-input/remove-prohibited.ts#L14) & [解释](https://forums.ankiweb.net/t/how-to-add-external-css-in-a-field/17838/9) ）
## 使用

复制src文件夹到插件文件夹即可，也可将其重命名为fastwq，啥都行。


# ENG
(Unexpectedly, there are non-Chinese users 😁)

Adapt to pyqt6

Adapt to anki new api

Modify invalid dictionary

Fix the problem that the css file cannot be loaded (temporarily valid) ([problem source](https://github.com/ankitects/anki/blob/main/ts/editor/plain-text-input/remove-prohibited.ts#L14) & [Explanation](https://forums.ankiweb.net/t/how-to-add-external-css-in-a-field/17838/9) )
## Use

Just copy the src folder to the plugin folder, or rename it to fastwq, whatever.



# -------------------


# FastWordQuery Addon For Anki

  [Supported Dictionaries](docs/services.md)

  [为单词添加真人发音（朗文mdx词典）](docs/get_mdx_ldoce6_sounds.md)



## Features

This addon query words definitions or examples etc. fields from local or online dictionaries to fill into the Anki note.  
It forks from [WordQuery](https://github.com/finalion/WordQuery), added **multi-thread** feature, improve stability, and some other features.

  - Querying Words and Making Cards, IMMEDIATELY!
  - Support querying in mdx and stardict dictionaries.
  - Support querying in web dictionaries.
  - Support **Multi-Thread** to query faster.

## Install

   1. Just copy the src folder to the plugin folder, or rename it to fastwq, whatever.



## Setting

### Shortcut
  1. Click Menu **"Tools -> Add-ons -> FastWQ -> Edit..."**  
      ![](screenshots/setting_menu.png)
  2. Edit the code and click **Save**  
      ![](screenshots/setting_shortcut.png)

### Config
  1. In Browser window click menu **"FastWQ -> Options"**  
      ![](screenshots/setting_config_01.png)

  2. Click **Settings** button in the Options window  
      ![](screenshots/setting_config_02.png)  
      - **Force Updates of all fields** : Update all fields even if it's None
      - **Ignore Accents** : Ignore accents symbol of word in querying
      - **Auto check new version** : Check new version at startup
      - **Number of Threads** : The number of threads running at the same time
  
  
## Usage

### Set the query fields

  1. Click menu **"Tools ->  FastWQ"**, or in Browser window click menu **"FastWQ -> Options"**
  2. Select note type  
      ![](screenshots/options_01.png)
  3. Select Dictionary  
      ![](screenshots/options_02.png)
  4. Select Fields  
      ![](screenshots/options_03.png)
  5. Click **OK** button  

### 'Browser' Window
  1. Select single or multiple words, click menu **"FastWQ -> Query Selected"** or press shortcut Default is **Ctrl+Q**.  
      ![](screenshots/options_04.png)
  2. Waiting query finished  
      ![](screenshots/use_01.png)
  
### 'Add' Window
  1. Click Add button in Browser window, open Add window  
      ![](screenshots/use_02.png)
  2. Edit key field and click Query button  
      ![](screenshots/use_03.png)


## Other Projects Used
  - [mdict-query](https://github.com/mmjang/mdict-query)
  - [pystardict](https://github.com/lig/pystardict)
  - [WordQuery](https://github.com/finalion/WordQuery)
  - [AnkiHub](https://github.com/dayjaby/AnkiHub)
  - [snowball_py](https://github.com/shibukawa/snowball_py)
