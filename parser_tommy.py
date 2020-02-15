from bs4 import BeautifulSoup
import requests
import random
import time
import re
from model import *
import os

proxy = {'HTTPS': '163.172.182.164:3128'}
url = 'https://www.macys.com/shop/womens-clothing/calvin-klein-dresses?id=62066&edge=hybrid'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
}
cookies = {
    'shippingCountry': 'US',
    'currency': 'USD'
}
cat_url_list = []
url_list = []
color_list = []
size_list = []
details_list = []

Session = sessionmaker(bind=db_engine)
session = Session()


def read_file_url():
    with open('input_tommy.txt', 'r') as file:
        for line in file:
            cat_url_list.append(line.strip('\n'))
    return cat_url_list


def get_html(url, payload=None):
    while True:
        time.sleep(random.randint(random.randint(6, 10), random.randint(12, 27)))
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


def get_url_category(html):
    # функция которая парсит все ссылки с категории товара
    soup = BeautifulSoup(html.content, 'html.parser')
    link_list = soup.find('div', class_='sortableGrid').find_all('li', class_='cell')
    for i in link_list:
        try:
            url = i.find('a', class_='productDescLink')['href']
            url_list.append('https://www.macys.com/' + url)
        except:
            continue
    return url_list


def get_page_count(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    try:
        page_count = soup.find('select', id='select-page').find_all('option')[-1]['value']
        return int(page_count)
    except:
        page_count = 1
        return int(page_count)


def parser_card(html, image_name):
    soup = BeautifulSoup(html.content, 'html.parser')
    try:
        # название товара
        name = soup.find('h1', class_='p-name h3').text.strip()
    except:
        name = ''
    try:
        # парсинг полной цены
        full_price = soup.find('div', class_='price').text.strip()
        price = re.findall(r'\d*[.]\d+', full_price)[0]
    except AttributeError:
        try:
            full_price = soup.find('div', class_='on-sale').text.strip()
            price = re.findall(r'\d*[.]\d+', full_price)[0]
        except:
            price = None
            with open('price_error.txt', 'a') as write_file:
                write_file.writelines(html.url)
    try:
        # цена с скидкой
        sale_price = soup.find('span', {'data-auto': 'sale-price'}).text.strip()
        discount_price = re.findall(r'\d*[.]\d+', sale_price)[0]
    except:
        discount_price = None
    try:
        # процент скидки
        percent_text = soup.find('span', {'data-auto': 'percent-off'}).text.strip()
        percent = re.findall(r'\d+', percent_text)[0] + '%'
    except:
        percent = None
    try:
        # категория товара
        category = soup.find_all('a', class_='breadcrumbs-item')
        cat_name = category[1].text + '/' + category[2].text
    except:
        cat_name = None
    try:
        #парсим цвета
        c_list = soup.find_all('li', class_='color-swatch')
        for i in c_list:
            try:
                color_tag = i.find('div', class_='color-swatch-div')['aria-label']
                color_list.append(color_tag)
            except:
                continue
    except:
        color_list.append('')
    try:
        color_tag = soup.find('div', class_='color-header').find('strong').text
    except:
        color_tag = None
    try:
        color = color_list[0]
    except:
        color = None
    try:
        # парсим размеры
        ul = soup.find('ul', class_='medium-float-children swatches-scroller c-reset').find_all('li')
        for li in ul:
            if li['aria-disabled'] == 'false':
                size_list.append(li.text.strip())
    except:
        try:
            size_tag = soup.find('strong', {'data-auto': 'selected-size'}).text.strip()
            size_list.append(size_tag)
        except:
            size_list.append('')

    try:
        details = soup.find('ul', {'data-auto': 'product-description-bullets'}).find_all('li')
        for i in details:
            details_list.append(i.text)
    except:
        details_list.append('')
    url = html.url
    try:
        new_element = MacysTommy(name, price, discount_price, percent, cat_name, color,','.join(color_list), ','.join(size_list),
                            ','.join(details_list), ','.join(image_name), url)
        session.add(new_element)
        session.commit()
    except:
        with open('errorTommy.txt', 'a') as write_file:
            write_file.writelines(html.url)
    color_list.clear()
    size_list.clear()
    details_list.clear()
    image_name.clear()


def create_dir_name():
    dir_name = 'imagesTommy'
    try:
        os.mkdir(dir_name)
    except OSError:
        print('Папка существует')
    return dir_name


def chek_images():
    # проверяет номер последней фото в папке, и при запуске парсера след фото будет +1
    num_file = []
    last_image = 0
    try:
        file_list = os.listdir('imagesTommy')
        for list in file_list:
            num_file.append(int(re.findall(r'\d*', list)[0]))
        num_file.sort()
        print(num_file[-1])
    except(IndexError):
        num_file.append(0)
    last_image = num_file[-1]
    return int(last_image) + 1


def get_photo(html, dir_name):
    img_name = []
    image_list = []
    payload = {
        'size': 'small',
        'clientId': 'PROS',
        '_shoppingMode': 'SITE',
        '_customerState': 'GUEST',
        'currencyCode': 'USD',
        '_regionCode': 'US'
    }
    sub_url_1 = 'https://slimages.macysassets.com/is/image/MCY/products/'
    sub_url_2 = '?op_sharpen=1&wid=1230&hei=1500&fit=fit,1&$filterxlrg$'
    api_url = 'https://www.macys.com/xapi/digital/v1/product/'
    soup = BeautifulSoup(html.content, 'html.parser')
    ul = soup.find('ul', {'data-auto': 'product-description-bullets'}).find_all('li')[-1].text
    id = re.findall(r'\d+', ul)
    response = requests.get(api_url + id[0], headers=HEADERS, proxies=proxy, cookies=cookies, params=payload)
    for img in response.json()['product'][0]['imagery']['images']:
        image_url = sub_url_1 + img['filePath'] + sub_url_2
        image_list.append(image_url)
    for img in image_list:
        try:
            last_img = chek_images()
            count_photo = last_img
            photo_name = count_photo
            file_obj = requests.get(img, stream=True)
            if file_obj.status_code == 200:
                with open(dir_name + '/' + str(photo_name) + '.JPG', 'bw') as photo:
                    for chunk in file_obj.iter_content(8192):
                        photo.write(chunk)
                img_name.append(str(photo_name))
        except:
            print('Error file_obj')
    return img_name



def main():
    count = 1
    dir_name = create_dir_name()
    cat_url_list = read_file_url()
    for cat_url in cat_url_list:
        html = get_html(cat_url)
        page_count = get_page_count(html)
        for i in range(1, page_count+1):
            page_idex = '/Pageindex/'
            sub_url = cat_url.split('?')
            link = sub_url[0] + page_idex + str(i) + '?' + sub_url[1]
            html = get_html(link)
            url_list = get_url_category(html)
    print(f'Всего товаров для парсинга{len(url_list)}')
    for url in url_list:
        card_exist = session.query(MacysTommy.url).filter(MacysTommy.url == url).count()
        if not card_exist:
            html = get_html(url)
            image_name = get_photo(html, dir_name)
            parser_card(html, image_name)
            print(f'Всего товаров для парсинга {len(url_list)} спарсили {count}')
            count += 1
        else:
            count += 1
            print('Этот товар есть в базе, пропускаем')


if __name__ == '__main__':
    main()
