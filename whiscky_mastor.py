import requests
import json
import re
from bs4 import BeautifulSoup
import pandas as pd
import sys
from datetime import datetime
import jieba

Alcohol_name = []
Alcohol_winery = []
Alcohol_url = []
Alcohol_years = []
Alcohol_loct = []
Alcohol_ABV = []
Alcohol_content = []
Alcohol_contect = []
Alcohol_price = []
Alcohol_img = []

url = ('https://www.masterofmalt.com/country/scotch-whisky/')
headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Referer": "https://www.masterofmalt.com/country/scotch-whisky/"
           }
cookies = {}

res_url = requests.get(url , headers=headers)
#print(res_url.text)

soup_url = BeautifulSoup(res_url.text, 'html.parser')
#print(soup_url)

title_list = soup_url.select('ul[title="Distilleries links"]>li>a')
for title_url in title_list:
    #print(title_url)
    title = title_url.text
    print(title)
    title_url_res = 'https://www.masterofmalt.com' + str(title_url).split('"')[1]
    print(title_url_res)
    res_brand_url = requests.get(title_url_res , headers=headers)
    soup_brand_url = BeautifulSoup(res_brand_url.text , 'html.parser')
    #print(soup_brand_url)
    alcohol_title = soup_brand_url.select('div[class="col-md-12"]>div>h3>a')
    #print(alcohol_title)
    for alcohol_title_url in alcohol_title:
        title_url_list = str(alcohol_title_url).split('"')[1]
        print(title_url_list)
        res_alcohol = requests.get(title_url_list, headers=headers)
        soup_alcohol = BeautifulSoup(res_alcohol.text, 'html.parser')
        #print(soup_alcohol)
        Years = '1900'
        print('======================================')
        alcohol_name = soup_alcohol.select('div[class="row"]>div>h1')[0].text
        print(alcohol_name)
        try:
            alcohol_ABV = soup_alcohol.select('div[class="row"]>div>span')[0].text.split(' ')[1].split(')')[0]
            print(alcohol_ABV)
        except IndexError as e:
            continue
        alcohol_img = 'https:' + str(soup_alcohol.select('div[class="productImageWrap"]')[0]).split('src')[1].split('"')[1]
        print(alcohol_img)
        alcohol_content = soup_alcohol.select('div[itemprop="description"]')[0].text
        print(alcohol_content)
        try:
            alcohol_price = soup_alcohol.select('div[class="product-price gold"]')[0].text
            print(alcohol_price)
        except IndexError as e :
            print('NT$')
            continue
        alcohol_contect_list = soup_alcohol.select('p[itemprop="reviewBody"]')
        for j in alcohol_contect_list:
            alcohol_contect = j.text
        print(alcohol_contect)

        Alcohol_name.append(alcohol_name)
        Alcohol_winery.append(title)
        Alcohol_url.append(title_url_list)
        Alcohol_years.append(Years)
        Alcohol_loct.append('Scotch')
        Alcohol_ABV.append(alcohol_ABV)
        Alcohol_content.append(alcohol_content)
        Alcohol_contect.append(alcohol_contect)
        Alcohol_price.append(alcohol_price)
        Alcohol_img.append(alcohol_img)

df = pd.DataFrame(
    {'酒名': Alcohol_name, '酒廠': Alcohol_winery, '網址': Alcohol_url, '年分': Alcohol_years, '產地': Alcohol_loct,
     '酒精度': Alcohol_ABV, '內容': Alcohol_content, '評論': Alcohol_contect, '價格': Alcohol_price, '照片': Alcohol_img})
df.to_csv("whiscky_scoV2.csv", index=False, sep='+')