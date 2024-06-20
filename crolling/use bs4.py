import os
import time
import requests
import urllib.request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from io import BytesIO

# 이미지 저장 경로 설정
keyword = "참외"
save_dir = os.path.join(os.getcwd(), keyword)
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)

# ChromeDriver 경로 설정
webdriver_path = 'C:\\Users\\kimes\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'  # 실제 chromedriver 경로로 변경하세요

# Selenium 웹드라이버 설정
options = webdriver.ChromeOptions()
service = Service(executable_path=webdriver_path)
driver = webdriver.Chrome(service=service, options=options)

# Google 이미지 검색 페이지 열기
url = "https://www.google.com/search?q=%EC%B0%B8%EC%99%B8&sca_esv=d5d0c4751fe7bdbd&sca_upv=1&hl=ko&authuser=0&tbm=isch&sxsrf=ADLYWILoo0hS-SnFCbrHh5oxV1hDodwI8g%3A1718907984828&source=hp&biw=1152&bih=585&ei=UHR0ZsX5MOmpvr0PvYK42Q4&iflsig=AL9hbdgAAAAAZnSCYM3lw8BJAjB1-uyJ9AZmSwjmjtM6&ved=0ahUKEwjF4dee5-qGAxXplK8BHT0BLusQ4dUDCA8&uact=5&oq=%EC%B0%B8%EC%99%B8&gs_lp=EgNpbWciBuywuOyZuDIEECMYJzIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABEiPGVDJAViwF3AHeACQAQCYAXOgAcAIqgEEMC4xMLgBA8gBAPgBAYoCC2d3cy13aXotaW1nmAIOoALhBqgCCsICBxAjGCcY6gLCAgsQABiABBixAxiDAcICCBAAGIAEGLEDwgIOEAAYgAQYsQMYgwEYigWYAxSSBwM3LjegB8Aw&sclient=img"
driver.get(url)

before_h = driver.execute_script("return window.scrollY")

# 무한스크롤
while True:
    time.sleep(2)
    # 맨 아래로 스크롤을 내림
    driver.find_element(By.CSS_SELECTOR,"body").send_keys(Keys.END)
    
    # 스크롤 후 높이
    after_h = driver.execute_script("return window.scrollY")
    
    # 스크롤 높이가 맨 아래와 같다면 무한루프 탈출
    if after_h == before_h:
        break

    # 스크롤 높이 업데이트
    before_h = after_h

# 페이지 소스 가져오기
page_source = driver.page_source
driver.quit()

# BeautifulSoup을 사용하여 이미지 태그 파싱
soup = BeautifulSoup(page_source, 'html.parser')
img_tags = soup.select("img")

# 이미지 다운로드
n = 0
for img in img_tags:
    try:
        src = img.get('src')
        if src is None:
            src = img.get('data-src')
        
        if src and src.startswith('http'):
            # 이미지 크기 확인
            response = requests.get(src)
            image = Image.open(BytesIO(response.content))
            width, height = image.size
            
            if width >= 100:
                urllib.request.urlretrieve(src, os.path.join(save_dir, str(n) + '.jpg'))
                print(f"Image {n} saved.")
                n += 1
            else:
                print(f"Image {n} skipped due to small width ({width}px).")
    except (ValueError, HTTPError, URLError, requests.RequestException, IOError) as e:
        print(f"Error downloading image {n}: {e}")

print("다운로드 완료")
