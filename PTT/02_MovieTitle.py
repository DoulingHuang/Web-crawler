import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
url = 'https://www.ptt.cc/bbs/movie/index.html'


res = requests.get(url, headers=headers)

soup = BeautifulSoup(res.text, 'html.parser')
#print(soup)

title_list = soup.select('div[class="title"]')
#print(title_list)

for title_soup in title_list :
    title = title_soup.select('a')[0].text
    print(title)
    title_url = 'https://www.ptt.cc' + title_soup.select('a')[0]['href']
    print(title_url)