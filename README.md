# Dazzled-Darling
Final Project of [Web Retrieval and Mining spring 2018](https://www.csie.ntu.edu.tw/~pjcheng/course/wm2018/)

[![Packagist](https://img.shields.io/badge/TensorFlow-1.10.1-orange.svg)]()
[![Packagist](https://img.shields.io/badge/Keras-2.2.2-blue.svg)]()
[![Packagist](https://img.shields.io/badge/Python-3.5.0-blue.svg)]()
[![Packagist](https://img.shields.io/badge/MacOS-10.13.1-black.svg)]()
## 迷惘美 Dazzled-Darling
* 一個專屬於你的網美檢索系統
* 健全的資料庫 (1559位IG網美，每位100篇圖/文)
* 任意輸入關鍵字找尋有興趣的主題
* 能依據你的喜好(e.g.性感, 旅行,...)來客製化檢索結果

## Flowchart
![](https://github.com/kevinisbest/Dazzled-Darling/blob/master/images/flowchart.001.jpeg)

## Requirements
* Python 3.X
* Keras==2.0.8
* numpy==1.14.0
* gensim==3.4.0
* tqdm==4.19.5
* scipy==0.19.0
* Pillow==5.1.0

## Usage
* **Note**: Our system only support Traditional Chinese query. If you are in MacOS, tkinter not support the MacOS orginal Traditional Chinese input, you only can type your query in another place and copy/paste. 

1. First, download our [WordCount1.npy](https://github.com/kevinisbest/Dazzled-Darling/releases/download/AllWordCount1.npy/allWordCount1.npy.gz) and extract it under **data/**.
2. Run the code.
```
cd src/
python3 gui.py
```

## Demo
![](https://github.com/kevinisbest/Dazzled-Darling/blob/master/images/Demo.gif)

## Authors
* [kevinisbest](https://github.com/kevinisbest)
* [Shanboy5566](https://github.com/Shanboy5566)
* [ayueh0822](https://github.com/ayueh0822)
* [ryannnchenholiao](https://github.com/ryannnchenholiao)
