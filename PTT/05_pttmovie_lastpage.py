import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

url = 'https://www.ptt.cc/bbs/movie/index.html'

for i in range(0 , 3):
    res = requests.get(url , headers=headers)

    soup = BeautifulSoup(res.text , 'html.parser')
    #print(soup)

    title_list = soup.select('div.title')
    #print(title_list)

    for i in title_list:

        try:

            title = i.select('a')[0].text
            title_url = 'https://www.ptt.cc' + i.select('a')[0]['href']
            print(title)
            print(title_url)
        except IndexError as e :
            print(e)

    page_soup = 'https://www.ptt.cc' + soup.select('a[class="btn wide"]')[1]['href']
    #print(page_soup)

    url = page_soup