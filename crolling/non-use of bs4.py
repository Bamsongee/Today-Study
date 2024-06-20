from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib.request
import requests
from PIL import Image
from io import BytesIO
import time
import os

# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요 메세지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 옵션 적용
browser = webdriver.Chrome(options=chrome_options)
keyword = "참외 사진"

save_dir = os.path.join(os.getcwd(), keyword)
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)

path = f'https://www.google.com/search?q={keyword}&sca_esv=581612012&tbm=isch&sxsrf=AM9HkKnRu6DCGGz23e29xT4BSB7Hq95zgA:1699754235522&source=lnms&sa=X&ved=2ahUKEwiboaf7rb2CAxWJfd4KHWkWA9MQ_AUoAXoECAQQAw&biw=1552&bih=737&dpr=1.65' # 구글
browser.implicitly_wait(5)
browser.maximize_window()
browser.get(path)

before_h = browser.execute_script("return window.scrollY")

# 무한스크롤
while True:
    time.sleep(2)
    # 맨 아래로 스크롤을 내림
    browser.find_element(By.CSS_SELECTOR,"body").send_keys(Keys.END)
    
    # 스크롤 후 높이
    after_h = browser.execute_script("return window.scrollY")
    
    # 스크롤 높이가 맨 아래와 같다면 무한루프 탈출
    if after_h == before_h:
        break

    # 스크롤 높이 업데이트
    before_h = after_h

images = browser.find_elements(By.TAG_NAME, "img")
print(images)

links = []
for image in images:
    src = image.get_attribute('src')
    if src is None:
        src = image.get_attribute('data-src')
    if src is not None:
        links.append(src)

print('찾은 이미지의 개수 : ', len(links))

# 이미지 다운로드
for k, url in enumerate(links):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        width, height = image.size

        if width >= 100:
            urllib.request.urlretrieve(url, os.path.join(save_dir, f'{keyword}_{k}.jpg'))
            print(f"Image {k} saved. Width: {width}")
        else:
            print(f"Image {k} skipped due to small width ({width}px).")
    except Exception as e:
        print(f"Failed to save image {k}: {e}")

print('다운로드를 완료하였습니다.')
browser.quit()
