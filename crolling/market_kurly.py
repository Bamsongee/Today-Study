from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests as req

# https://www.kurly.com/categories/908

# 크롬드라이버 경로 설정
driver_path = 'C:\\Users\\kimes\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'

# ChromeOptions 객체 생성
chrome_options = Options()

# ChromeDriver 서비스 객체 생성
service = Service(driver_path)

# ChromeDriver 초기화
driver = webdriver.Chrome(service=service, options=chrome_options)

# 특정 웹 페이지 열기
driver.get('https://www.kurly.com/categories/908')

# 가격 찾기
price_list = []
elements = driver.find_elements(By.CLASS_NAME, 'price-number')
for element in elements:
    price_list.append(element.text)

# 품목명 찾기
title_list = []
elements = driver.find_elements(By.CLASS_NAME, 'css-1dry2r1.e1c07x485')
for element in elements:
    title_list.append(element.text)

# 가격과 품목 딕셔너리로 합치기
karliy_data = []
for price, title in zip(price_list, title_list):
    karliy_data.append({price, title})

print(karliy_data)

# 브라우저 닫기
driver.quit()

# 출력 내용
# [{'23,900', '[KF365] 당도선별 수박 4kg 이상'}, {'당도선별 성주 참외 1.5kg (4~7입)', '19,900'}, {'[KF365] 대추방울토마토 750g', '11,900'}, {'[KF365] 당도선별 수박 5kg 이상', '9,900'}, {'7,990', '[KF365] 국산 블루베리 200g (특)'}, {'[KF365] DOLE 실속 바나나 2종', '6,990'}, {'고랭지 부사 사과 1.3kg (4~5입)', '17,900'}, {'땅끝 해남 쌀 10kg', '9,990'}, {'[KF365] 당도선별 수박 6kg 이상', '8,990'}, {'국산 블루베리 100g (특)', '3,990'}, {'[수미과] 조각 수박 800g', '3,391'}, {'청송 사과 1.5kg (5~7입)', '24,900'}, {'22,900', '[스윗볼] 스테비아 토마토 3종'}, {'35,900', '[KF365] 머스크멜론 1.6kg'}, {'성주 꼬마 참외 900g (5~8입)', '23,900'}, {'조선향미 8kg', '18,900'}, {'완숙토마토 1kg', '6,990'}, {'5,990', '[KF365] 방울토마토 500g'}, {'19,900', '[KF365] 유명산지 고당도사과 1.5kg (5~6입)'}, {'미국산 캘리포니아 생체리 300g (9.5row)', '17,910'}, {'31,900', '조선향미 쌀 4kg'}, {'29,900', '벌이 수정한 퇴촌 완숙찰토마토'}, {'8,900', '냉동  칠레산 블루베리 1kg'}, {'임금님표 이천쌀 알찬미 쌀 10kg', '7,900'}, {'11,900', '[제스프리] 뉴질랜드 골드키위 1.1kg (8~10입) (후숙필요)'}, {'9,900', '[Dole] 아보카도 1kg (5~7입)'}, {'[Dole] 스위티오 바나나 1kg', '7,980'}, {'친환경 블루베리 100g (특)', '51,000'}, {'친환경 블루베리 300g (상)', '6,490'}, {'5,990', '하우스 감귤 800g'}, {'5,490', '[제스프리] 뉴질랜드 골드 키위 760g (4입X2팩) (후숙필요)'}, {'4,990', '[KF365] 친환경 블루베리 200g (특)'}, {'29,900', '친환 경 대추방울토마토 500g'}, {'12,900', '달보드레쌀 4kg'}, {'9,900', '[KF365] 완숙토마토 2kg'}, {'세척사과 1.4kg (7입)', '26,900'}, {'7,990', '[스위프리] 스테 비아 토마토 3종'}, {'무농약 마틸다 토마토 1kg', '6,990'}, {'11,900', '[fruit salon] 컷팅 파인애플 1kg'}, {'10,900', '씻어나온 완전미 고시히카리 쌀 4kg'}, {'44,900', '무농약 토마토 1kg'}, {'13,900', '영광 신동진 쌀 10kg'}, {'스테비아 대추방울토마토 450g', '10,990'}, {'11,900', '델라웨어 포도 200g'}, {'주스용 실 속 사과 2kg', '5,190'}, {'[KF365] 새콤달콤 제주 감귤 1.5kg', '8,100'}, {'세지 멜론 1.2kg', '6,900'}, {'델라웨어 포도 500g', '14,900'}, {'작지만 나도 성주 참외 2kg', '16,900'}, {'13,900', '유기농 바나나 500g'}, {'12,900', '[KF365] 아보카도 (1개)'}, {'[썬키스트] 팬시 레몬 1kg (8-12입)', '12,900'}, {'8,690', '[수 미과] 조각 수박 400g'}, {'유기농 혼합 9곡 800g (콩없는 혼합 잡곡)', '6,990'}, {'유명산지 머스크 멜론 1.6kg', '16,900'}, {'10,900', '시나노골드 (금사과) 1.3kg (5~7입)'}, {'9,900', '[Dole] 스위티오 파인애플 슬라이스 540g'}, {'조선향미 현미 1kg', '24,900'}, {'8,900', '유기농 경조정 500g'}, {'[귤로장생] 제주 하우스 감귤 1kg', '11,900'}, {'10,900', '조선향미 쌀 1kg'}, {'12,900', '백진주 쌀 4kg'}, {'19,900', '유기농 담음 신동진 쌀 4kg'}, {'11,900', '유기농 경조정 200g'}, {'엘그로 백진주쌀 10kg', '9,900'}, {'38,900', '초여름 제철 과일 골라담기 5종'}, {'(특)신비 복숭아 700g', '7,900'}, {'거봉 포도 450g', '6,900'}, {'유기농  찰토마토 2kg', '6,990'}, {'5,990', '냉동 트리플 베리 1kg (칠레산)'}, {'[KF365] 스미후루 감숙왕 바나나 2종', '29,900'}, {'냉동 딸기 1kg (국산)', '27,900'}, {'27,900', '[썬키스트] 팬시 레몬 300g (3입)'}, {'유기농 블루베리 100g (특)', '24,900'}, {'12,900', '구운 아몬드 500g'}, {'10,900', '[KF365] 당도선별 수박 7kg 이상'}, {'유레카 블루베리 100g 3종 (택1) (국산)', '15,900'}, {'13,900', '40일동안 맛볼 수 있는 경조정과 델라웨어 600g'}, {'[HBAF] 매일 색다른 먼투썬 하루견과 2주 (20gX14봉)', '14,900'}, {'3,790', '유명산지 배 2kg (3~4입)'}, {'[치키타] 바나나 1.2kg', '2,990'}, {'2,490', '백미 10kg 골라담기 8종'}, {'태국산 마하 차녹 무지개 망고 600g (2입)', '11,000'}, {'11,900', '[Dole] 스위티오 파인애플 청크 400g'}, {'10,710', '[KF365] 밥상의 진미 쌀 4kg'}, {'냉동 유기농 블루베리 700g (미국산)', '9,990'}, {'14,900', '임금님표 이천쌀 알찬미 쌀 4kg'}, {'[귤림원] 당도선별 GAP 하우스 감귤 500g', '12,900'}, {'21,900', '맛나 대추방울토마토 750g'}, {'10,900', '냉동 아보카도 500g (페루산)'}, {'HBAF 매일 색다른 먼투썬 하루견과 6주 (20gX42봉)', '7,890'}, {'매일견과 블루베리 플러스 360g', '25,900'}, {'태국산 망고 620g (2입)', '23,900'}, {'18,900', '유기농 밀키퀸 쌀2종'}, {'17,900', '네뷸라 토마토 750g'}, {'하루 건강견과 Excellent 500g (20gX25봉)', '8,490'}]햣