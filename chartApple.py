from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

# 웹드라이브 설치(수동)
# browser = webdriver.Chrome()
# browser.get("https://www.music-flo.com/browse")

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
folder_path = "appleMusic"
filename = f"{folder_path}/appleChart100_{current_date}.json"

# 웹드라이브 설치
options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.get("https://music.apple.com/kr/playlist/%EC%98%A4%EB%8A%98%EC%9D%98-top-100-%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD/pl.d3d10c32fbc540b38e266367dc8cb00c")

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "songs-list"))
)

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# 노래 정보를 추출
song_data = []
songs_list = soup.find_all('div', class_='songs-list-row', role='row')

for song in songs_list:
    ranking = song.find('div', class_='songs-list-row__rank').text.strip()
    title = song.find('div', class_='songs-list-row__song-name').text.strip()
    artist = song.find('a', {'data-testid': 'click-action'}).text.strip()
    album = song.find_all('a', {'data-testid': 'click-action'})[1].text.strip()
    img_tag = song.find('picture').find('source', type="image/webp")  # More specific targeting to webp images
    if img_tag:
        image_sources = img_tag['srcset']
        # Extracting the desired 80x80 webp image URL from srcset
        image_url = next((src.split(' ')[0] for src in image_sources.split(',') if '80x80bb.webp' in src), "No image available")
    else:
        image_url = "No image available"

    song_data.append({
        'ranking': ranking,
        'title': title,
        'artist': artist,
        'album': album,
        'image_url': image_url
    })

# 추출된 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(song_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()