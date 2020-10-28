import requests
from bs4 import BeautifulSoup
import os

if not os.path.exists('pttmovie'):
    os.mkdir('pttmovie')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

url = 'https://www.ptt.cc/bbs/movie/index{}.html'

page = 8975
for i in range(0 , 1):

    try:

        res = requests.get(url.format(page), headers=headers)

        soup = BeautifulSoup(res.text, 'html.parser')
        #print(soup)

        title_list = soup.select('div[class="title"]')
        #print(title_list)

        for title_soup in title_list :
            title = title_soup.select('a')[0].text
            print(title)
            title_url = 'https://www.ptt.cc' + title_soup.select('a')[0]['href']
            print(title_url)

            artical_url = 'https://www.ptt.cc' + title_soup.select('a')[0]['href']
            res_title = requests.get(artical_url , headers=headers)
            res_title_soup = BeautifulSoup(res_title.text , 'html.parser')
            #print(res_title_soup)
            content = res_title_soup.select('div[id="main-content"]')[0].text.split('※ 發信站')[0]
            print(content)
            # try:
            #     with open('./pttmovie/%s.txt' % (title), 'w', encoding='utf-8') as f:
            #         f.write(content)
            # except FileNotFoundError as e:
            #     print(e)
            #     print(title)
            #     with open('./pttmovie/%s.txt' % (title.replace('/' , '')), 'w', encoding='utf-8') as f:
            #         f.write(content)
    except IndexError as e :
        print(e)




    page -= 1