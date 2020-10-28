import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

url = 'https://www.ptt.cc/bbs/Gossiping/index.html'

cookies = {'over18' : '1'}
a = 0
for i in range(0 , 1):
    res = requests.get(url  , cookies=cookies , headers=headers)

    soup = BeautifulSoup(res.text , 'html.parser')
    #print(soup)

    title_list = soup.select('div.title')
    #print(title_list)

    for title_soup in title_list:
        try:
            title = title_soup.select('a')[0].text
            title_url = 'https://www.ptt.cc' + title_soup.select('a')[0]['href']
            a += 1
            print(a)
            print(title)
            print(title_url)
        except IndexError as e:
            print(e)

last_page = 'https://www.ptt.cc' + soup.select('a[class="btn wide"]')[1]['href']
#print(last_page)

url = last_page