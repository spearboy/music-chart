import requests
from bs4 import BeautifulSoup
import datetime
import json

def get_chart_data(url):
    # 사용자 에이전트 설정
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    
    # 웹 페이지로부터 데이터 요청 및 수신
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")

    # 데이터 선택
    chart_data = []
    rows = soup.select("tbody > tr.list")

    for row in rows:
        rank = row.select_one("td.number").contents[0].strip()
        image_url = row.select_one("td a.cover img").get('src').replace('//', 'https://')
        title = row.select_one("td.info a.title.ellipsis").text.strip()
        artist = row.select_one("td.info a.artist.ellipsis").text.strip()
        album = row.select_one("td.info a.albumtitle.ellipsis").text.strip()

        chart_data.append({
            "rank": rank,
            "title": title,
            "artist": artist,
            "imageUrl": image_url,
            "album": album
        })

    return chart_data

current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# 두 페이지의 URL
urls = [
    "https://www.genie.co.kr/chart/top200?ditc=D&ymd=20240428&hh=19&rtm=Y&pg=1",
    "https://www.genie.co.kr/chart/top200?ditc=D&ymd=20240428&hh=19&rtm=Y&pg=2"
]

# 모든 페이지에서 차트 데이터 가져오기
all_chart_data = []
for url in urls:
    chart_data = get_chart_data(url)
    all_chart_data.extend(chart_data)

# JSON 파일로 저장
folder_path = "genieMusic"
file_name = f"{folder_path}/genieChart100_{current_date}.json"

with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(all_chart_data, file, ensure_ascii=False, indent=4)