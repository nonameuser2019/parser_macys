from bs4 import BeautifulSoup
import requests
import random
import time
from selenium import webdriver
import re

proxy = {'HTTPS': '157.245.224.29:3128'}
url = 'https://www.macys.com/shop/product/calvin-klein-off-the-shoulder-sheath-dress?ID=10491609&CategoryID=62066&swatchColor=Blossom%20Pink&swatchColor=Blossom%20Pink'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'
}
cat_url_list = []
cookies = {
    'shippingCountry': 'US',
    'currency': 'USD'
}
html = requests.get(url, headers=HEADERS, proxies=proxy, cookies=cookies)
print(html.status_code)
soup = BeautifulSoup(html.content, 'html.parser')
# full_price = soup.find('div', class_='price').text.strip()
# price = re.findall(r'\d*[.]\d+', full_price)[0]
# sale_price = soup.find('div', {'data-auto': 'with-offer-phone'}).text.strip()
# discount_price = re.findall(r'\d*[.]\d+', sale_price)[0]
#
# color_list = soup.find_all('li', class_='color-swatch')
# for i in color_list:
#     print(i)
# print(color_list)
ul = soup.find('ul', {'data-auto' : 'product-description-bullets'}).find_all('li')[-1].text
id = re.findall(r'\d+',ul)

main_url = 'https://www.macys.com/xapi/digital/v1/product/'
payload = {
    'size': 'small',
    'clientId': 'PROS',
    '_shoppingMode': 'SITE',
    '_customerState': 'GUEST',
    'currencyCode': 'USD',
    '_regionCode': 'US'
}
response = requests.get(main_url+id[0], headers=HEADERS, proxies=proxy, cookies=cookies, params=payload)
print(response.status_code)

