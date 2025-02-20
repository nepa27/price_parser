import json
import os
import re

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from log_config import logger


load_dotenv('.env')
key_price = os.getenv('FLAG_PRICE_LIME')
tag_price = os.getenv('TAG_PRICE_LIME')
key_list_price_lime = os.getenv('KEY_LIST_PRICE_LIME')
key_price_lime = os.getenv('KEY_PRICE_LIME')
key_name_lime = os.getenv('KEY_NAME_LIME')


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
            data = soup.find_all(string=re.compile(key_price_lime))
            json_data = json.loads(data[0])
            name_thing = json_data[key_name_lime]
            main_price = json_data[key_list_price_lime][key_price_lime]
        # print(f'Название: {name_thing}')
        # print(f'Цена: {main_price}')
        logger.info(f'Спарсены данные {name_thing, main_price}')
        return name_thing, main_price
    except BaseException as er:
        print(f'Возникла ошибка: {er}')
