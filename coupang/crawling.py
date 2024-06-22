import requests
import re
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def getProducts(string):
    bsObj = BeautifulSoup(string, "html.parser")
    # print(bsObj)

    productList = bsObj.find("ul", {"class":"common_sp_list_ul ea4"})
    # print(productList)

    products = productList.findAll("li", {"class":"common_sp_list_li"})

    for item in products:
        #url
        a = item.find("a", {"class": "common_sp_link"})
        url = "https://m.10000recipe.com" + a.get('href')
        print("url:", url)

        # image
        image = a.find("img").get('src')
        print("image:", image)

        #name
        div_name = item.find("div", {"class":"common_sp_caption_tit line2"})
        name = div_name.getText()
        print("name:", name)

    print(len(products))
    return []

# 마켓컬리 채소 카테고리
url = "https://www.10000recipe.com/ranking/home_new.html"

# 크롤링 차단 해결
# options.add_argument("--disable-blink-features=AutomationControlled")

# SSL 경고 무시
warnings.simplefilter('ignore', InsecureRequestWarning)

# url에 get 요청
def getPageString(url):
    data = requests.get(url, headers = headers, verify=False)
    data.raise_for_status()
    return data.content

# print(getPageString(url))
pageString = getPageString(url)
print(getProducts(pageString))