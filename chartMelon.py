import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime

current_date = datetime.datetime.now().strftime("%Y-%m-%d")
res = req.get("https://www.melon.com/chart/index.htm")
soup = bs(res.text, "lxml")

# 데이터 선택
ranking = soup.select("tbody .rank")
title = soup.select(".wrap_song_info > .rank01 > span > a")
artist = soup.select(".wrap_song_info > .rank02 > span > a:nth-child(1)")

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
file_name = f"melonChart100_{current_date}.json"
chart_df.to_json(file_name, force_ascii=False, orient="records")
