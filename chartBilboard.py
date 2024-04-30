import requests
from bs4 import BeautifulSoup
import json
import datetime

# 현재 날짜를 문자열로 저장
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# 웹 페이지로부터 데이터 요청 및 수신
res = requests.get("https://www.billboard.com/charts/hot-100/")
soup = BeautifulSoup(res.text, "lxml")

# print(res.text)
# print(res.status_code) 

# 데이터 선택
ranking = soup.select(".o-chart-results-list-row-container > ul > li.o-chart-results-list__item:nth-child(1) > span.c-label:nth-child(1)")
title = soup.select(".o-chart-results-list-row-container > ul > li.lrv-u-width-100p > ul > li:nth-child(1) > h3.c-title")
artist = soup.select(".o-chart-results-list-row-container > ul > li.lrv-u-width-100p > ul > li:nth-child(1) > span.c-label")
image = soup.select(".o-chart-results-list-row-container ul > li:nth-child(2) .c-lazy-image > div > img")

# print(len(image))

# 데이터 저장
rankings = [r.text.strip() for r in ranking]
titles = [t.text.strip() for t in title]
artists = [a.text.strip() for a in artist]
images = [img.get('data-src') or img.get('data-lazy-src') or img.get('src') for img in image]

# print(images)

# 데이터 프레임 생성
chart_data = []
for ranking, title, artist, image_url in zip(rankings, titles, artists, images):
    chart_data.append({
        "rank": ranking,
        "title": title,
        "artist": artist,
        "imageURL": image_url
    })

# 파일 이름 설정
file_name = f"billMusic/billboardChart100_{current_date}.json"

# JSON 파일로 저장
with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(chart_data, file, ensure_ascii=False, indent=4)
