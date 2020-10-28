import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

url = 'https://www.ptt.cc/bbs/movie/index.html'

for i in range(0, 5):
    # HTML String
    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text, 'html.parser')

    title_list = soup.select('div.title')
    # print(title_list)

    for title_soup in title_list:
        # print(title_soup)
        try:
            title = title_soup.select('a')[0].text
            titl_url = 'https://www.ptt.cc' + title_soup.select('a')[0]['href']
            print(title)
            print(titl_url)
        except IndexError as e:
            print(title_soup)

    # Get last-page url
    page_url_soup = soup.select('a[class="btn wide"]')
    # print(page_url_soup)
    last_page_url = 'https://www.ptt.cc' + page_url_soup[1]['href']
    # print(last_page_url)

    url = last_page_url