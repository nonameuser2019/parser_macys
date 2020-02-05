from bs4 import BeautifulSoup
import requests
import random
import time
from selenium import webdriver
import re

# proxy = {'HTTPS': '157.245.224.29:3128'}
# url = 'https://www.macys.com/shop/product/calvin-klein-ruffled-collar-scuba-sheath-dress-regular-petite-sizes?ID=5379688&CategoryID=5449&swatchColor=Black#fn=BRAND%3DCalvin%20Klein'
#
# HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'
# }
# cat_url_list = []
# cookies = {
#     'shippingCountry': 'US',
#     'currency': 'USD'
# }
# html = requests.get(url, headers=HEADERS, proxies=proxy, cookies=cookies)
# print(html.status_code)
# soup = BeautifulSoup(html.content, 'html.parser')
#
# image_url = 'https://slimages.macysassets.com/is/image/MCY/products/4/optimized/15393744_fpx.tif?op_sharpen=1&wid=500&hei=613&fit=fit,1&$filtersm$'
x = '(46% off)'
y = re.findall(r'\d+', x)
print(y[0]+'%')

