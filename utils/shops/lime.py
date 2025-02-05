import json
import os
import re

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from utils.request import get_page

load_dotenv('.env')
key_price = os.getenv('FLAG_PRICE_LIME')
tag_price = os.getenv('TAG_PRICE_LIME')
key_list_price_size = os.getenv('KEY_LIST_PRICE_LIME')
key_price_size = os.getenv('KEY_PRICE_LIME')


def parse_lime(response):
    """Парсит цену на товар в LIME."""
    soup = BeautifulSoup(response, 'lxml')

    try:
        try:
            _ = soup.find('h1')
            name_thing = _.find_next('h1').text
            prices = soup.find_all(tag_price, string=re.compile(key_price))
            main_price = prices[1].text.rstrip(key_price)
        except:
            data = soup.find_all(string=re.compile(key_price_size))
            main_price = json.loads(data[0])[key_list_price_size][key_price_size]
        print(f'Название: {name_thing}')
        print(f'Цена: {main_price}')
    except BaseException as er:
        print(f'Возникла ошибка: {er}')


with open('lime_sale.html', 'r') as f:
    file = f.read()

# parse_lime(get_page('https://lime-shop.com/ru_ru/product/21901_9983_688-sero_koricnevyi'))
parse_lime(file)