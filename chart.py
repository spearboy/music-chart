import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd

res = req.get("https://music.bugs.co.kr/chart")

# print(res.text)
# print(res.status_code)

soup = bs(res.text, "lxml")
# print(soup)

ranking = soup.select(".ranking > strong")
title = soup.select(".title > a")
artist = soup.select(".artist > a:nth-child(1)")
# print(ranking)
# print(title)
# print(artist)
# print(len(ranking))
# print(len(title))
# print(len(artist))

# rankingList = []
# titleList = []
# artistList = []

# for i in range(len(ranking)) :
#     rankingList.append(ranking[i].text)
#     titleList.append(title[i].text)
#     artistList.append(artist[i].text)

# print(rankingList)
# print(artistList)
# print(titleList)

# data = {"rank" : rankingList, "title": titleList, "artist": artistList}

# print(pd.DataFrame(data))

rankingList = [r.text.strip() for r in ranking]
titleList = [t.text.strip() for t in title]
artistList = [a.text.strip() for a  in artist]

chart_df = pd.DataFrame({
    'Ranking' : rankingList,
    'Title' : titleList,
    'Artist' : artistList
})

file_name = f"bugsChart100_{current_date}.json"
chart_df.to_json(file_name, force_ascii=False, orient="records")
