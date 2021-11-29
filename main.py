import json
from extract_news import extract_max_pages

print("원하는 날짜 입력 : ", end="")
date = input()
max_pages = extract_max_pages(date)
