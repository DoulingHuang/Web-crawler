import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

url = 'https://www.ptt.cc/bbs/Gossiping/index.html'

cookies = {'over18' : '1'}

a = 0
n = 1
for i in range(0 , n):
    res = requests.get(url  ,cookies=cookies  , headers=headers)

    soup = BeautifulSoup(res.text , 'html.parser')
    #print(soup)

    title_list = soup.select('div.title')
    #print(title_list)

    for title_soup in title_list:
        try:
            title = title_soup.select('a')[0].text
            title_url = 'https://www.ptt.cc' + title_soup.select('a')[0]['href']
            a += 1
            print('========================================================')
            print(a)
            print(title)
            print(title_url)

            res_content= requests.get(title_url, cookies=cookies, headers=headers)
            soup_content = BeautifulSoup(res_content.text , 'html.parser')
            #print(soup_content)
            content = soup_content.select('div[id="main-content"]')[0].text.split('--')[0]
            print(content)
            print('---split---')

            push_url = soup_content.select('div[class="push"] span')
            # print(push_url)
            push_up = 0
            push_down = 0
            for info in push_url:
                if '推' in info.text:
                    push_up += 1
                if '噓' in info.text:
                    push_down += 1
            print('推 : ', push_up)
            print('噓 : ', push_down)
            score = push_up - push_down
            print('分數 : ', score)

            author_list = soup_content.select('div[class="article-metaline"]')[0]
            #print(author_list)
            author_name = author_list.select('span[class="article-meta-value"]')[0].text
            print('作者 : '  ,author_name)
            content_title = soup_content.select('div[class="article-metaline"]')[1]
            # print(author_list)
            content_title_name = content_title.select('span[class="article-meta-value"]')[0].text
            print('標題 : ', content_title_name)
            time_title = soup_content.select('div[class="article-metaline"]')[2]
            # print(author_list)
            time_title_name = time_title.select('span[class="article-meta-value"]')[0].text
            print('時間 : ', time_title_name)




        except IndexError as e:
            print(e)

last_page = 'https://www.ptt.cc' + soup.select('a[class="btn wide"]')[1]['href']
#print(last_page)

url = last_page