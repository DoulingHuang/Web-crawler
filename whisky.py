import requests
from bs4 import BeautifulSoup
from urllib import parse
import datetime
import os
import pandas as pd
import time
import csv
import re

url = 'https://thewhiskyphiles.com/whisky-reviews/whisky-scores/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
res = requests.get(url=url, headers=headers)
res.encoding = "utf-8"
soup = BeautifulSoup(res.text, 'html.parser')
# print(res)
# print(soup)

Japan_URL = soup.select('li.cat-item-507046 a')[0]['href'] #日本威士忌37種
scotch_URL = soup.select('li.cat-item-1418205 a')[0]['href'] #蘇格蘭威士忌1270種
us_URL = soup.select('li.cat-item-16944253 a')[0]['href']
world_URL = soup.select('li.cat-item-35483995 a')[0]['href']



#Ireland #愛爾蘭威士忌61種
for page in range(1,8): #共有7頁
    Ireland_URL = soup.select('li.cat-item-465311 a')[0]['href'] + 'page/{}'.format(str(page))
    # IrelandURL = Ireland_URL.format(str(page))
    res = requests.get(url=Ireland_URL, headers=headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, 'html.parser')
    whisky = soup.select('div#main-content h2.posttitle')
    for wh in whisky:#每一款酒的評論連結  主要資訊都在這
        url = wh.select('a')[0]['href'] #連結
        res = requests.get(url=url, headers=headers)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, 'html.parser')
        name = soup.select('h1[class="title"]')[0].text
        # print(name)

        #先抓整個ul的標籤，然後再用正則表示法去篩選目標字串
        whisky = soup.select_one('section.entry').select_one('ul').text #酒的類別
        print(type(whisky))
        pattern1 = re.compile('Category.*')
        pattern2 = re.compile('ABV.*')
        pattern3 = re.compile('factory.*')
        pattern4 = re.compile('years.*')
        pattern5 = re.compile('price.*')
        Category = pattern1.findall(whisky)[0]
        print(Category)
        #用sibling 去抓下一層標籤(內容、評論)

        # print(Category)
        # print(type(Category))
        # ABV = soup.select('section.entry li')[0].text.split(':')[1] #標籤不一致
        # print(ABV)
    #     picture_url=
        # content=
        # conment =soup.select('section.entry ul li')[0].text
        # print(conment)
        # factory = soup.select('section.entry li')[5].text.split(':')[1] #爬網頁origin的部分 非裝瓶廠
        # years = soup.select('section.entry li')[1].text.split(':')[1].replace('NAS','null') #釀製年份
        # original= soup.select('a.post-lead-category')[0].text #產地 愛爾蘭酒 = 愛爾蘭?
        # # Category = soup.select('section.entry li')[3].text.split(':')[1]#酒的類別
        # price = soup.select('section.entry li')[0].text.split(':')[1]










