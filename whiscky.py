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
loctation = {'scotch', 'japanese', 'american', 'irish', 'canadian', 'world'}
loctation2 = {'japanese'}
for L in loctation2:
    url = ('https://www.connosr.com/scotch-whisky')
    headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Referer": "https://www.connosr.com/{}-whisky".format(L)
               }
    cookies = {
        '_ga' : 'GA1.2.1137145689.1592230630',
        '_gid' : 'GA1.2.326891135.1592230630'}

    res_url = requests.get(url , cookies=cookies, headers=headers)
    #print(res_url.text)
    soup_url = BeautifulSoup(res_url.text, 'html.parser')
    #print(soup_url)
    for i in range(100):
        try:
            brand_url = 'https://www.connosr.com' + soup_url.select('a[class="name"]')[i]['href']
            #print(brand_url)
            res_brand_url = requests.get(brand_url, cookies=cookies, headers=headers)
            soup_brand_url = BeautifulSoup(res_brand_url.text, 'html.parser')
            #print(soup_brand_url)
            for j in range(100):
                title_url_list = 'https://www.connosr.com' + soup_brand_url.select('div[class="horizontal-scrolling-inner"]>ul>li>a')[j]['href']
                print(title_url_list)
                title_res = requests.get(title_url_list, cookies=cookies, headers=headers)
                title_soup = BeautifulSoup(title_res.text, 'html.parser')
                #print(title_soup)
                title = title_soup.select('div[class="simple-header"]>h1')[0].text
                #print(title)
                Brand = title_soup.select('div[class="product-info-block"]>ul>li')[0].text.split(': ')[1]
                #print(Brand)
                #print(L)
                try:
                    ABV = title_soup.select_one('abbr[title="Alcohol by Volume"]').next_sibling.next_sibling.text
                    #print(ABV)
                except AttributeError as f:
                    continue
                Deteil = str(title_soup.select('span[class="data"]'))
                rr = re.compile(r'\w\w year old', re.I)  # 不區分大小寫
                print(type(rr))
                Years = rr.findall(Deteil)
                print(type(Years))
                print(Years)
                Content = '略'
                Price = 'XXXXXXXXX'
                img = 'https://www.connosr.com'+ title_soup.select('img[class="image not-mobile"]')[0]['src']
                #print(img)
                #r1 = r'Bottled: '
                # font = re.findall(r1 , 'Bottled: ').
                # print(font)
                Contect = title_soup.select('article[class="simple-review cf"]>div>p')
                for k in Contect:
                    print(k.text)

                Alcohol_name.append(title)
                Alcohol_winery.append(Brand)
                Alcohol_url.append(title_url_list)
                Alcohol_years.append(Years)
                Alcohol_loct.append(L)
                Alcohol_ABV.append(ABV)
                Alcohol_content.append(Content)
                Alcohol_contect.append(k.text)
                Alcohol_price.append(Price)
                Alcohol_img.append(img)

        except IndexError as e:
            continue

df = pd.DataFrame({'酒名':Alcohol_name , '酒廠':Alcohol_winery, '網址':Alcohol_url, '年分':Alcohol_years, '產地':Alcohol_loct, '酒精度':Alcohol_ABV, '內容':Alcohol_content, '評論':Alcohol_contect, '價格':Alcohol_price, '照片':Alcohol_img})
df.to_csv("whiscky_sco.csv", index=False, sep='/')