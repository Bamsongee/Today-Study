from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import mysql.connector
from mysql.connector import Error

# https://www.kurly.com/categories/908

# 크롬드라이버 경로 설정
driver_path = 'D:\\chromedriver\\chromedriver-win64\\chromedriver.exe'

# ChromeOptions 객체 생성
chrome_options = Options()

# ChromeDriver 서비스 객체 생성
service = Service(driver_path)

# ChromeDriver 초기화
driver = webdriver.Chrome(service=service, options=chrome_options)

# 특정 웹 페이지 열기
driver.get('https://www.kurly.com/categories/908')

before_h = driver.execute_script("return window.scrollY")



# 가격 찾기
price_list = []
elements = driver.find_elements(By.CLASS_NAME, 'price-number')
for element in elements:
    price_list.append(element.text)


    # private String imageUrl;
    # private String name;
    # private String discript;
    # private int salePercent;
    # private int originalPrice;
    # private int salePrice;

# 이미지 찾기
image_list = []
elements = driver.find_elements(By.CLASS_NAME, 'css-1zjvv7')
for element in elements:
        src = element.get_attribute("src")
        image_list.append(src)

# 품목명 찾기
title_list = []
elements = driver.find_elements(By.CLASS_NAME, 'css-1dry2r1.e1c07x485')
for element in elements:
    title_list.append(element.text)

# 설명 찾기
discript_list = []
elements = driver.find_elements(By.CLASS_NAME, 'css-1wejlc3.e1c07x483')
for element in elements:
    discript_list.append(element.text)

# 퍼센트 찾기
percent_list = []
elements = driver.find_elements(By.CLASS_NAME, 'discount-rate.css-19lkxd2.ei5rudb0')
for element in elements:
    percent_list.append(element.text)

# 원가 찾기
original_price = []
elements = driver.find_elements(By.CLASS_NAME, 'price-number')
for element in elements:
    original_price.append(element.text)

# 세일 가격 찾기
sale_price = []
elements = driver.find_elements(By.CLASS_NAME, 'price-number')
for element in elements:
    sale_price.append(element.text)

# 가격과 품목 딕셔너리로 합치기
kurly_datas = []
for image, title, discript, percent, price in zip(image_list, title_list, discript_list, percent_list, original_price):
    kurly_datas.append({
        "image": image,
        "title": title,
        "description": discript,
        "percent": percent,
        "price": price
    })

print(kurly_datas)

# 브라우저 닫기
driver.quit()

connection = None

# MySQL 데이터베이스에 연결
try:
    connection = mysql.connector.connect(
        host='localhost',  # MySQL 서버 주소
        database='ohmea',  # 데이터베이스 이름
        user='root',  # MySQL 사용자 이름
        password='km923009!!'  # MySQL 비밀번호
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # 테이블 생성
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            image TEXT,
            title TEXT,
            description TEXT,
            percent TEXT,
            price TEXT
        )
        ''')

        # 데이터 삽입
        for data in kurly_datas:
            cursor.execute('''
            INSERT INTO products (image, title, description, percent, price)
            VALUES (%s, %s, %s, %s, %s)
            ''', (data['image'], data['title'], data['description'], data['percent'], data['price']))

        # 커밋하고 연결 종료
        connection.commit()
        print("데이터 저장 성공")
        cursor.close()
        connection.close()
        print("MySQL 연결 종료")

except Error as e:
    print(f"Error: {e}")