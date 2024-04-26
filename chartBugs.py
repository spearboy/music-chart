import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime

current_date = datetime.datetime.now().strftime("%Y-%m-%d")
res = req.get("https://music.bugs.co.kr/chart")
soup = bs(res.text, "lxml")

# 데이터 선택
ranking = soup.select(".ranking > strong")
title = soup.select(".title > a")
artist = soup.select(".artist > a:nth-child(1)")

# 데이터 저장
rankingList = [r.text.strip() for r in ranking]
titleList = [t.text.strip() for t in title]
artistList = [a.text.strip() for a in artist]

# 데이터 프레임 생성
chart_df = pd.DataFrame({
    'Ranking': rankingList,
    'Title': titleList,
    'Artist': artistList
})

# JSON 파일로 저장
file_name = f"bugsChart100_{current_date}.json"
chart_df.to_json(file_name, force_ascii=False, orient="records")
