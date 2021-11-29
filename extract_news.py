from sys import maxsize
from bs4 import BeautifulSoup
import requests


headers = headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}

# 날짜별로 최대 기사 페이지 수를 리턴


def extract_max_pages(date):
    last = False
    max_pages = 0
    i = 1
    while last == False:
        news_url = "https://news.daum.net/breakingnews/politics?page={}&regDate=" + date
        res = requests.get(news_url.format(i))
        html = BeautifulSoup(res.text, "html.parser")
        paging = html.find("div", class_="paging_news").find(
            "span", class_="inner_paging")
        pages = paging.find_all('a')[-1]
        nextBtn = pages.find('span', class_="ico_news")
        i += 10
        if nextBtn is None:
            max_pages = pages.get_text()
            break
    return max_pages
