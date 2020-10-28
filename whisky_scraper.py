import requests, os ,urllib, json,time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib import request
import csv
# jieba.load_userdict('E:/EB102_PYETL/res_104/104_dict.txt')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'cookie': 'wblang=eyJpdiI6ImRVVk9zV09KbDhYSWVkaFdsTHk1aUE9PSIsInZhbHVlIjoiXC92NzBmNGRucnhYVUM4emIyUXQ2cFE9PSIsIm1hYyI6ImU5YWYyNGJiN2MyN2Q5MzkwMDljOGE1M2UzMzJkYTllY2RhY2FjMDg4NTdlMmQ5MjdkMjkxOWY0OWI2YjQyMTAifQ%3D%3D; _ga=GA1.2.1159201967.1592310282; _gid=GA1.2.535349044.1592310282; wbts=eyJpdiI6IitNRVNDTzZEcmxvZGVxb0lUdWhFR3c9PSIsInZhbHVlIjoiZjBDNEdLS0VNQlJLVXlQVDkxNlR1UT09IiwibWFjIjoiMTEzOTk1ZjhkNDI2NjM1ZTlkMTEwMGE1YmUyMDMzMmVkN2Q2MzhlMGM5YmVlMmMxN2VlMjdiODg4ZDZmYTIwMCJ9; XSRF-TOKEN=eyJpdiI6ImJRSis4SUJOSUF1WXNBOVRJUDlZWGc9PSIsInZhbHVlIjoiakJJWk9IVXZVUFJUbWw1TnNPa3RmS1RIc0w3WXd3ZVFOMlhnY3huYUp4R281XC9qYjdoMk9OdHd4VW5sM29cL0kxQTl4YnQzWFhWdnkxMk40OHRROHdxQT09IiwibWFjIjoiZjQ2ZWYyNzRiZTdmNGRjZTIzOWZhMzU4OTc5Y2RhNjIwM2UxNGNjMDhlMjU5N2VlMzg4MzZhYWQ5ZTY1NWMxOSJ9; barrel=eyJpdiI6IisraEtxZ3F0ZXppR1B2dDlxV0lrOXc9PSIsInZhbHVlIjoicjBzcEFwY2xqV3lRZXVOMVZFbWRod1JhSTFoUGR6WWJFcmtEeWRJZkxLOGduMndVUmdiaTR2XC8wSCtLSW52UE5raTlTTVlNZ0wzYm9jelBBcTJKbEJBPT0iLCJtYWMiOiI0ZjJjYTNiN2FkYWExYWVlYjc0OWNkMjQ4ODVlMjI4MmFjNjUyNjE1YTlkNDU3NGE5MGFmZDQxZDQ2OTQ5MGQ3In0%3D'}
# url = 'https://www.whiskybase.com/whiskies/whisky/149985/dailuaine-2011-82nc'
url = 'https://www.whiskybase.com/whiskies/new-releases'
res = requests.get(url=url, headers= headers)
soup = bs(res.text,'html.parser')

# title = soup.find('table')
# print(title)
# a=pd.read_html(url)[0]
# print(a)
# 年分
# whisky_years = title.find_all('td',{'class':"data text-right"})
# for whisky_year in whisky_years:
#     print(whisky_year.text)
# whisky_year = title.find_all(class_= 'data text-right')

# print(whisky_years[1].text)
# print(whisky_year.text)
# a = whisky2_list.find_next_sibling('td')
# for whisky_year in whisky2_list:
#     a=whisky_year.find_next_sibling('td')
#     print(whisky_year)
#酒精度(%)
# whisky_abv = whisky_years.find_next_siblings('td')
# print(whisky_abv)
'''test1
whisky_alcohol_content_list = soup.select('div[id="compositor-material"] td[class="data text-right"]')
td_list = whisky_alcohol_content_list.find_all("td")
a=whisky_alcohol_content_list[1:2]
print(td_list)
for whisky_alcohol_content in whisky_alcohol_content_list:
    w_alcohol = whisky_alcohol_content.find_next_siblings('td')
    a=(whisky_alcohol_content.find_next_sibling('td'))
    b=(a.find_next_siblings)
    print(whisky_alcohol_content[1:2])
    s=whisky_alcohol_content.find_next_siblings('td')[1]
    print(s)
    w_year = w_alcohol.find_next_siblings('td')
    print(w_year.text)
    print(whisky_alcohol_content.text.split('\n\n'))

whisky_alcohol_list = soup.find('tbody')
whisky_alcohol_rows = whisky_alcohol_list.select('tr')[1:]
print(whisky_alcohol_rows)
for whisky_alcohol_content in whisky_alcohol_rows:
    print(whisky_alcohol_content.text.split('\n\n')[3])
'''

columns =['酒名','酒廠','url','年分','產地','酒精度(%)','照片','內容','評論','價錢']
# 子分頁所需要的資料
article_title_html = soup.select('div[class="container-fluid"]')
WhiskyList = pd.DataFrame()
for each_article in article_title_html:
    try:
        whisky_list = soup.select('div[id="filter-host-content"] a[class="clickable"]')
        for whisky_url in whisky_list:
            # 1.名稱
            whisky_name =whisky_url.text
            print(whisky_name)
            # 3.目標網址url
            url=whisky_url['href']
            print(url)
            # resp = requests.get(whisky_url['href'])
            article_url = whisky_url['href']
            article_res = requests.get(url=article_url,headers=headers)
            soup2 = bs(article_res.text, 'html.parser')
            # 2.酒廠
            whisky_winery_list = soup2.select('div[id="whisky-distillery-list"] a')
            for whisky_winery in whisky_winery_list:
                winery=whisky_winery.text
            # 4.年分
            whisky_age = None
            # 5.產地
            region = None
            # 6.酒精度數
            whisky_abv = None
            # 7.照片
            whisky_img= soup2.select('div[class="carousel-inner"] a[class="photo"]')[0]['href']
            # 內容
            content = None
            # 評論
            whisky_comment_list = soup2.select('div[id="whisky-note-holder"] [class="wb--free-text"]')
            for whisky_comment in whisky_comment_list:
                 comment=whisky_comment.text
            #價格
            price = None
        time.sleep(0.5)

    except FileNotFoundError as e:
        pass
        tmp_list = [whisky_name, winery, url, whisky_age, region, whisky_abv, whisky_img, content, comment, price]
        # fine_list.append(tmp_list)

df = pd.DataFrame(columns=columns)
df = df.append(pd.DataFrame(WhiskyList, columns=columns))
WhiskyList

# save
df.to_csv(r'./WhiskyList.csv', index=None, encoding='utf-8')

print('done!')



