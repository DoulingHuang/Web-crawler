from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

file_data = (r'./whisky')
if not os.path.exists(file_data):
    os.mkdir(file_data)

driver = Chrome('.\chromedriver')

url_f = 'https://www.influenster.com/reviews/whiskey?brand=jack-daniels&brand=crown-royal&brand=jameson&brand=jim-beam&brand=johnnie-walker&brand=fireball-cinnamon-whisky&brand=wild-turkey&brand=glenfiddich&brand=makers-mark&brand=the-glenlivet&page={}'

# #brands
# brands = soup.select('a[data-category-filter="brand"]')
#
#
# for b in brands:
#      url_a = 'https://www.influenster.com/' + b["href"]
#      res = driver.get(url_a)
#      soup =  BeautifulSoup(driver.page_source, "html.parser")
#
#
#      print(url_a)
# 換頁
page = 1
df = pd.DataFrame(
    columns=["酒名","酒廠","url","年份","產地","酒精度(%)","照片","內容","評論","價錢"])

whisky_a = []
whisky_b = []
whisky_all = []
g = []
whisky = {"name": "", "winery": "","url":"","year":"","origin":"","concentration":"","image":"","content":"","reviews_total":"","price":""}

for p in range(0, 7):

    driver.get(url_f.format(page))

    soup = BeautifulSoup(driver.page_source, "html.parser")
    # ALCOHOLIC BEVERAGES
    whisky_url = soup.select('a.category-product')


    #每款酒的網址

    for w in whisky_url:
        url_w = 'https://www.influenster.com/' + w["href"]
        res = driver.get(url_w)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        whisky['url'] = url_w
        # time.sleep(2)
        print(whisky['url'])
        # print(w)

        #酒名
        name = soup.select('div[class="textComponents__TruncateText-sc-1463il4-0 eenUMx layoutComponents__Text-l2otzz-1 ijhpCt layoutComponents__Block-l2otzz-0 gfowDv"]')[0].text
        whisky['name'] = name
        # print(name)

        #酒廠
        whisky['winery'] = 'NULL'

        #年份
        whisky['year'] = 'NULL'

        #產地
        whisky['origin'] = 'NULL'

        #酒精度
        whisky['concentration'] = 'NULL'

        # 照片url
        image = soup.select('div[class="gallery__PreviewImageWrapper-sc-1ja997c-2 fUsGth"] ')[0].img["src"]
        whisky['image'] = image
        # print(image)

        #內容
        content_total = soup.select('div[class="with-more textComponents__TruncateText-sc-1463il4-0 eenUMx layoutComponents__Text-l2otzz-1 cdjhZn layoutComponents__Block-l2otzz-0 ixyxcj"]')
        # content = content_total[0].text
        if content_total == []:
            whisky['content'] = "NULL"
        else:
            whisky['content'] = content_total[0].text
        # print(whisky['content'])





        #價格
        whisky['price'] = 'NULL'

    # print(whisky_a)

        # 評論

        review = []
        reviews = soup.select('div[class="review-text layoutComponents__Text-l2otzz-1 kgitTG layoutComponents__Block-l2otzz-0 ixyxcj"]')

        for i in reviews:
            reviews_text_a = []
            reviews_text = i.text
            reviews_text_a.append(reviews_text)         #每一則評論單獨包在一個list
            review.append(reviews_text_a)               #同一款酒的所有評論,用一個list包住
            whisky['reviews_total'] = review

        print(review)
        print("-------------------------------------------")
        whisky_a = list(whisky.values())        #取每個網站的資訊
        whisky_b.append(whisky_a)       #將所有網站的資訊丟入同一個list中

    page += 1

# print(whisky_b)


#
dff=df.append(pd.DataFrame(whisky_b,columns=["酒名","酒廠","url","年份","產地","酒精度(%)","照片","內容","評論","價錢"]))
dff.to_csv(r'./whisky/liquor_whisky.csv',index=False,encoding="utf-8-sig")