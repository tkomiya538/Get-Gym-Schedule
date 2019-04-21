#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import time
import types

from bottle import get, route, run, static_file, template, redirect, request, TEMPLATE_PATH, jinja2_template as template
from bs4 import BeautifulSoup

baseURLs = ["http://www.sumidacity-gym.com/","https://www.koto-hsc.or.jp/sports_center3/"]
extension = ".pdf"
keywords= ["個人利用","体育館","体育室"]
urls = [
    "http://www.sumidacity-gym.com/guide/kojin/",
    "https://www.koto-hsc.or.jp/sports_center3/schedule/",
        ]
TEMPLATE_PATH.extend(['./views','./css','./images','./js'])

# htmlテンプレートに渡すリンク先URLを取得
@route('/')
def get_link():

    output=[]
    global downloadURLs
    downloadURLs = []
    
    # リンク取得先のWebサイトにリクエストを送信し、PDFのリンクURLを取得する
    for url in urls:
        
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        links = soup.findAll('a')

        # PDFのリンクURLを抽出
        for link in links:

            href = link.get('href')
            title = link.getText()

            for keyword in keywords:

                if href and extension and keyword in (href + title):
                    downloadURLs.append(href)

    # PDFのリンクとなるURLを補完・取得
    for downloadURL in downloadURLs:

        # 一秒スリープ
        time.sleep(1)

        for baseURL in baseURLs:
            if baseURL in downloadURL:
                linkURL = downloadURL
            else:
                linkURL = baseURL + downloadURL

            r = requests.get(linkURL)

            # 接続確認
            if r.status_code == 200:
                output.append(linkURL)
    
    #アウトプットとなる関数を定義
    for i in range(4):
        globals()["output%d" % i] = ""

    # リストからURLを一つずつ抽出
    j=0
    for link in output:
        globals()["output%d" % j ] = link
        j += 1
    
    # htmlテンプレートにリンク先URLを渡す
    return template('index', output0 = output0, output1 = output1, output2 = output2, output3 = output3)

#cssファイルをインポート
@get('/static/css/<filename:re:.*.css>')
def css(filename):
    return static_file(filename, root="static/css")

# Webページを作成する    
if __name__ == '__main__':
    #run(host="localhost", port=1042, debug=True, reloder=True)
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

