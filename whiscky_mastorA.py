import requests
import json
import re
from bs4 import BeautifulSoup
import pandas as pd
import sys
from datetime import datetime

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

for page in range(1, 105):
    url = ('https://www.masterofmalt.com/country-style/scotch/single-malt-whisky/'.format(page))
    headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Referer": "https://www.masterofmalt.com/country/scotch-whisky/"
               }
    resfirst_url = requests.get(url , headers=headers)
    #print(resfirst_url.text)
    soupfirst_url = BeautifulSoup(resfirst_url.text , 'html.parser')
    #print(soupfirst_url)

    alcohol_url = soupfirst_url.select('div[class="col-md-12"]>div>h3>a')
    #print(alcohol_url)

    for alcohol in alcohol_url:
        #print(alcohol)

        name = alcohol.text
        print(name)
        URL = str(alcohol).split('"')[1]
        print(URL)
        res_url = requests.get(URL , headers=headers)
        soup_url = BeautifulSoup(res_url.text , 'html.parser')
        #print(soup_url)
        Detail = str(soup_url.select('span[class="kv-val"]'))
        #print(Detail)
        try:
            Years = str(re.search(r'\w\w year old', Detail , re.M | re.I)).split('\'')[1]
            #print(Years)
        except IndexError as e:
            Years = 'None'
        try:
            Content = soup_url.select('div[itemprop="description"]>p')[0].text
            print(Content)
        except IndexError as e:
            Content = 'None'
            print('None')
        Contect =  soup_url.select('div[class="h-gutter row"]>div>div>div>div>div>p[itemprop="reviewBody"]')
        #print(Contect)
        if Contect :
            for i in Contect:
                Contectlist = i.text.replace('\n', ' ')
                print(Contectlist)
        else:
            Contectlist = 'None'
            #print('None')
        try:
            Price = str(soup_url.select('div[class="product-price gold"]>div')[0]).split('<span>')[-1].split('</span>')[0]
            #print(Price)
        except IndexError as e:
            #print('NT$')
            Price = 'NT$'
        try:
            IMG = 'https:' + soup_url.select('div[class="productImageWrap"]>img')[0]['src']
            print(IMG)
        except IndexError as e:
            IMG = 'None'
        res = r'<span class="kv-val".*?>(.*?%)</span>'
        mm = re.findall(res, Detail, re.S | re.M)
        #print(mm)
        for item in mm:
            #print(item)
            Location = item.split(',')[0].split('>')[1].split('<')[0]
            print(Location)
            Brand = item.split(',')[1].split('>')[2].split('<')[0]
            print(Brand)
            ABV = item.split(',')[-1].split('>')[1]
            print(ABV)

            Alcohol_name.append(name)
            Alcohol_winery.append(Brand)
            Alcohol_url.append(URL)
            Alcohol_years.append(Years)
            Alcohol_loct.append(Location)
            Alcohol_ABV.append(ABV)
            Alcohol_content.append(Content)
            Alcohol_price.append(Price)
            Alcohol_img.append(IMG)
            Alcohol_contect.append(Contectlist)

            pd.set_option('display.max_rows', 500)
            pd.set_option('display.max_columns', 500)
            pd.set_option('display.width', 1000)

            df = pd.DataFrame({'酒名':Alcohol_name ,'酒廠':Alcohol_winery,'網址':Alcohol_url,'年分':Alcohol_years,'產地':Alcohol_loct,'酒精度':Alcohol_ABV,'評論':Alcohol_contect,'價格':Alcohol_price,'照片':Alcohol_img,'內容':Alcohol_content})

            df.to_csv("whiscky21.csv", index=False, sep='*')








