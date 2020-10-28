import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os
import random
import time
import re

file_data = (r'./my9')
if not os.path.exists(file_data):
    os.mkdir(file_data)
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
url_fir = "https://www.my9.com.tw/collections/%E5%A8%81%E5%A3%AB%E5%BF%8C?page={}"

df = pd.DataFrame(columns=['酒名', '酒廠', 'URL', '年份', '產地', '酒精度(%)', '照片', '內容', '評論', '價錢'])

page = 1

list_final = []

for i in range(0, 37):
    res_fir = requests.get(url_fir.format(page), headers=headers)
    soup_first = BeautifulSoup(res_fir.text, "lxml")

    # list_one = {"en_name": "", "cn_name": "", "winery": "", "url": "", "year":"", "area": "", "alcohol": "", "photo": "", "content": "", "comment":"", "money":""}
    # list_one = {"en_name": "", "winery": "", "url": "", "year":"", "area": "", "alcohol": "", "photo": "", "content": "", "comment":"", "money":""}
    list_one = {"cn_name": "", "winery": "", "url": "", "year": "", "area": "", "alcohol": "", "photo": "",
                "content": "", "comment": "", "money": ""}

    my_list = []
    list_try = []


    price = []
    price_one = []
    # 從16產品外部網頁抓價格
    test1 = soup_first.select("div[class='product-details']")
    # print(test1)
    for  try1 in test1:
        # print(try1)
        try2=try1.select("span.money ")

        if try2==[]:
            continue
        else:
            try:
                price_one=try2[1].text
                # print(try2)
            except:
                price_one=try2[0].text
        price.append(price_one.replace("$",""))
    print(price)


    print("-------------page=", page)
    page_product = soup_first.select("a.product-info__caption ")
    t = 0
    p=0
    for o in page_product:
        html_a=o["href"]
        html_url="https://www.my9.com.tw"+html_a
        print(html_url)
        res = requests.get(html_url,headers=headers)
        # time.sleep(random.uniform(1, 3))
        # time.sleep(2)
        soup = BeautifulSoup(res.text, "lxml")


         #URL
        list_one["url"]=html_url

        #照片擷取
        photo = soup.find('div',{'class':'gallery-cell'})
        photo_url = "https://"+ photo['data-image-height'].split('//')[1].split('?')[0]
        list_one["photo"]=photo_url

        # #英文名字
        # en_name = soup.select("p[itemprop='name']")[0].text
        # list_one["en_name"]=en_name

        #中文名字
        cn_name = soup.select("h1.product_name")[0].text
        list_one["cn_name"] = cn_name

        # 價錢
        money = soup.select("span[class='was_price']")[0].text
        cell_money = soup.select("span[itemprop='price']")[0].text
        # print("p=", p)
        # print("money=", money)
        # print("cell_money=", cell_money)

        # 英文版
        # if list_one["en_name"] =="The Macallan Sherry Oak 30Y" or list_one["en_name"] =="The Macallan Edition No.1" or list_one["en_name"] =="The Balvenie Tun 1858" or list_one["en_name"] =="The Balvenie Tun 1858" or list_one["en_name"] =="Nikka Yoichi 10Y" or list_one["en_name"] =="Nikka Whisky Taketsuru Pure Malt 17 Years Slim Bottle":
        #     list_one["money"] = "NULL"
        #     p = p - 1
        # elif list_one["en_name"] =="Madeira Cask 25Y Triple Cask":
        #     list_one["money"]=money
        #     p=p-1

        #中文版
        if list_one["cn_name"] =="麥卡倫 雪莉桶30年(藍標木盒)" or list_one["cn_name"] =="麥卡倫 EDITION NO.1" or list_one["cn_name"] =="百富 1858(第四版)" or list_one["cn_name"] =="百富 1858(第一版)" or list_one["cn_name"] =="余市 10年威士忌" or list_one["cn_name"] =="竹鶴17年威士忌":
            list_one["money"] = "NULL"
            p = p - 1
        elif list_one["cn_name"] =="百富 25年經典三桶":
            list_one["money"]=money
            p=p-1

        elif cell_money == " 請電洽" :
            list_one["money"] = "NULL"
            p = p - 1
        elif cell_money == "價格: 請電洽" :
            list_one["money"] = price[p]
        elif len(money) > 0:
            list_one["money"] = price[p]

        elif money == "":
            list_one["money"] = price[p]
        p += 1
        # print("list_one['money']=", list_one["money"])

        #內容
        content = soup.select("div[class='product-collapse white-block'] ")



        q=[]
        h=[]
        for j in content:

            if j.text =='':
                continue
            q.append(j.text.replace(" 展開↓",""))
            # print(q)
            # h='，'.join(q)

            # print("h=",h)

        content_try = soup.select("div[id = 'whisky-tastingnotes']  ")
        content_other = []
        cont = []
        if len(content_try) > 0:
            for try_cont in content_try:
                if try_cont.text == []:
                    continue
                content_other.append(try_cont.text.replace("\n", "").replace("\t", "").replace("Whisky Tasting Notes威士忌品飲筆記","").replace("/", ",").replace("\xa0", ""))

        # print(content_other)

        if content_other==[]:

            contt = q

        else:
            contt = q+content_other


        if contt == []:
            list_one["content"] = "NULL"
        else:
            h = "".join(contt).replace(".，","，").replace(",","，").replace("\n","")

            try:
                s= h.split('，數量有限，贈完為止！(贈品示意圖如下)')[1]
                if s=="":
                    list_one["content"]="NULL"
                else:
                    list_one["content"]=s
            except:
                list_one["content"]=h


        # print(list_one["content"])
        # print(content)

        #品牌/酒莊國家& 判別
        try:
            r = soup.select("div.product-details-item ")[2].span.text
            temporary_c = soup.select("div.product-details-item ")[2].a.text
            # print(r)
            # print(temporary_c)
            if r == "國家":
                list_one["area"] = temporary_c
            elif r == "品牌/酒莊":
                list_one["winery"] = temporary_c
        except:
            pass

        # 品牌/酒莊 判別
        try:
            n = soup.select("div.product-details-item ")[3].span.text
            temporary = soup.select("div.product-details-item ")[3].a.text
            if n == "品牌/酒莊":
                list_one["winery"] = temporary

        except:
            pass

        # 酒精度&品牌/酒莊 判別
        list_one["alcohol"] ="NULL"
        try:
            m = soup.select("div.product-details-item ")[4].span.text
            temporary_a = soup.select("div.product-details-item ")[4].div.text.replace("%","")
            if m == "酒精度":
                print("m =", m)
                list_one["alcohol"] = temporary_a
            elif m == "品牌/酒莊":
                list_one["winery"] = temporary_a
        except:
            pass

        # 酒精度判別
        try:
            s = soup.select("div.product-details-item ")[5].span.text
            temporary_b = soup.select("div.product-details-item ")[5].div.text.replace("%","")
            if s == "酒精度":
                print("s =",s )
                list_one["alcohol"] = temporary_b
        except:

            pass

        #都沒有年份 所以設NULL
        list_one["year"]="NULL"

        # 都沒有評論 所以設NULL
        list_one["comment"] = "NULL"

        #如果沒有酒精度就設為空
        if list_one["alcohol"]==[]:
            list_one["alcohol"]="NULL"
        if list_one["alcohol"]=="":
            list_one["alcohol"]="NULL"

        # 如果沒有國家就設為空
        if list_one["area"]=="":
            list_one["area"]="NULL"

        print('list_one["alcohol"]=',list_one["alcohol"])

        list_try = list(list_one.values())
        my_list.append(list_try)


        t=t+1

    # print(my_list)
    list_final+=(my_list)

    page+=1

print(list_final)

dff=df.append(pd.DataFrame(list_final,columns=['酒名','酒廠','URL','年份','產地','酒精度(%)','照片','內容','評論','價錢']))
dff.to_csv(r'./my9/my9.csv',index=False,encoding="utf-8-sig")
