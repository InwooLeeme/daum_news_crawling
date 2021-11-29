import json
from extract_news import extract_article, extract_max_pages

print("원하는 날짜 입력 : ", end="")
date = input()
max_pages = extract_max_pages(date)
results = extract_article(max_pages, date)

# json 파일로 저장
with open('results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent='\t', ensure_ascii=False)
