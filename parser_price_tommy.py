from bs4 import BeautifulSoup
import requests
import random
import time
import re
from model import *
import os


proxy = {'HTTPS': '163.172.182.164:3128'}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
}
cookies = {
    'shippingCountry': 'US',
    'currency': 'USD'
}
cat_url_list = []

def read_file_url():
    with open('input.txt', 'r') as file:
        for line in file:
            cat_url_list.append(line.strip('\n'))
    return cat_url_list


def get_html(url, payload=None):
    while True:
        time.sleep(random.randint(random.randint(6, 10), random.randint(12, 27)))
        #time.sleep(2)
        html = requests.get(url, headers=HEADERS, proxies=proxy, params=payload, cookies=cookies)
        if html.status_code == 200:
            print(html.status_code)
            return html
        elif html.status_code == 403:
            print(html.status_code)
            print('weit to 100-180 sec')
            time.sleep(random.randint(100,280))
        else:
            time.sleep(random.randint(14, 27))
            print(html.status_code)
            continue


def get_page_count(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    try:
        page_count = soup.find('select', id='select-page').find_all('option')[-1]['value']
        return int(page_count)
    except:
        page_count = 1
        return int(page_count)


def parser_price(html):
    # функция которая парсит все ссылки с категории товара
    sub_url = 'https://www.macys.com/'
    soup = BeautifulSoup(html.content, 'html.parser')
    link_list = soup.find('div', class_='sortableGrid').find_all('li', class_='cell')
    for i in link_list:
        try:
            tag_a = i.find('a', class_='productDescLink')['href']
            url = sub_url + tag_a
            price_tag = i.find('span', class_='regular originalOrRegularPriceOnSale').text.strip()
            price = re.findall(r'\d*[.]\d+', price_tag)[0]
            try:
                discount_tag = i.find('span', class_='discount').text.strip()
                discount = re.findall(r'\d*[.]\d+', discount_tag)[0]
            except:
                discount = None
            Session = sessionmaker(bind=db_engine)
            session = Session()
            new_element = MacysPriceTommy(price, discount, url)
            session.add(new_element)
            session.commit()
        except:
            continue




def main():
    cat_url_list = read_file_url()
    for cat_url in cat_url_list:
        html = get_html(cat_url)
        page_count = get_page_count(html)
        for i in range(1, page_count+1):
            page_idex = '/Pageindex/'
            sub_url = cat_url.split('?')
            link = sub_url[0] + page_idex + str(i) + '?' + sub_url[1]
            html = get_html(link)
            parser_price(html)


if __name__ == '__main__':
    main()