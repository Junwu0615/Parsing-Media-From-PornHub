<a href='https://github.com/Junwu0615/Parsing-Media-From-PornHub'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/Parsing-Media-From-PornHub.svg'> 
<a href='https://github.com/Junwu0615/Parsing-Media-From-PornHub'><img alt='GitHub Clones' src='https://img.shields.io/badge/dynamic/json?color=success&label=Clone&query=count_total&url=https://gist.githubusercontent.com/Junwu0615/c5c70b3f72648a0bc59f2a7a530b3e32/raw/Parsing-Media-From-PornHub_clone.json&logo=github'> </br>
[![](https://img.shields.io/badge/Project-Web_Crawler-blue.svg?style=plastic)](https://github.com/Junwu0615/Parsing-Media-From-PornHub) 
[![](https://img.shields.io/badge/Project-Parsing_Media-blue.svg?style=plastic)](https://github.com/Junwu0615/Parsing-Media-From-PornHub) 
[![](https://img.shields.io/badge/Language-Python_3.12.0-blue.svg?style=plastic)](https://www.python.org/) </br>
[![](https://img.shields.io/badge/Package-Requests_2.31.0-green.svg?style=plastic)](https://pypi.org/project/requests/) 
[![](https://img.shields.io/badge/Package-ArgumentParser_1.2.1-green.svg?style=plastic)](https://pypi.org/project/argumentparser/) 

## STEP.1　CLONE
```python
git clone https://github.com/Junwu0615/Parsing-Media-From-PornHub.git
```

## STEP.2　INSTALL PACKAGES
```python
pip install -r requirements.txt
```

## STEP.3　RUN
```python
python Entry.py -h 
```

## STEP.4　HELP

- `-h` Help : Show this help message and exit.
- `-u` URL : Give a <mdeia.m3u8> of PornHub `default: ''`
- `-p` Path : Give a save path | ex: './Media/' `default: Media`

## STEP.5　EXAMPLE

### I　執行前須注意事項
- 環境可能需要安裝 [FFmpeg](https://www.ffmpeg.org/download.html) 解包套件，請參考先前專案 [Parsing-Media-From-JVID](https://github.com/Junwu0615/Parsing-Media-From-JVID)
- 在想要抓得影片頁面，開啟`開發人員工具 (F12)`，搜尋`m3u8`，如下圖所示。

  - ![00.jpg](/Sample/00.jpg) 
  
  - 該長串網址即為要輸入進命令列的目標指令

  - ![00.gif](/Sample/00.gif) 
  
### II　範例
```python
python Entry.py -u [xxxxxxxxxxx]
```