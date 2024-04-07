"""extract html"""
from sys import maxsize
from bs4 import BeautifulSoup
import requests


headers = headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}

# 날짜별로 최대 기사 페이지 수를 리턴


def extract_max_pages(date):
    """extract max pages in date"""
    last = False
    max_pages = 0
    i = 1
    #while last == False: 수정전
    while last is False:
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

# 리포터 이름만 추출


def extract_reporter(url : str) -> str:
    """extract report function"""
    res = requests.get(url, timeout=10)
    html = BeautifulSoup(res.text, "html.parser")
    header = html.find("div", class_="head_view")
    repoter = header.find("span", class_="txt_info").get_text()
    return repoter

# 해당 기사의 본문 추출


def extract_body(url : str) -> list:
    """extract body and return list"""
    res = requests.get(url, timeout=10)
    html = BeautifulSoup(res.text, "html.parser")
    contents = html.find("div", class_="article_view").find(
        "section").find_all('p')[:-1]
    lists = []
    for p in contents:
        lists.append(p.text)
    return lists


def extract_article(max_pages, date) -> list:
    "extract article and return news"
    news = []
    NEWS_URL = "https://news.daum.net/breakingnews/politics?page={}&regDate=" + date
    limit_pages = int(max_pages) + 1
    for page in range(1, limit_pages):
        res = requests.get(NEWS_URL.format(page), headers=headers)
        if res.status_code == 200:
            print(f'page : {page}')
            html = BeautifulSoup(res.text, "html.parser")
            cont = html.find('ul', class_="list_news2 list_allnews")
            try:
                items = cont.findAll('li')
            except AttributeError as e:
                print(str(e))
                break
            else:
                for item in items:
                    article = item.find('strong', class_="tit_thumb")
                    title = article.a
                    article_info = article.find(
                        "span", class_="info_news").get_text()
                    article_url = title['href']
                    reporter = extract_reporter(article_url)
                    article_body = [extract_body(article_url)]
                    news.append({
                        'page': page,  # 해당 기사가 있는 페이지
                        'title': title.get_text(strip=True),  # 기사 제목
                        'url': article_url,  # 기사 url
                        # 언론사
                        'company': article_info[:5].replace('·', '').strip(),
                        # 올라온 시간
                        'time': article_info[5:].replace('·', '').strip(),
                        'reporter': reporter,  # 해당 기사를 작성한 사람
                        "body": article_body  # 기사의 본문
                    })
        else:
            break
    return news
