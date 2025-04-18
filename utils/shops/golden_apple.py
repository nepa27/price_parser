import json
import os
import re

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from log_config import logger


load_dotenv('.env')
key_price = os.getenv('FLAG_PRICE_GA')
tag_price_volume = os.getenv('TAG_PRICE_VOLUME_GA')
tag_volume = os.getenv('TAG_VOLUME_GA')

tag_all_data = os.getenv('TAG_ALL_DATA')
key_all_data = os.getenv('KEY_ALL_DATA')
begin_price_key = os.getenv('BEGIN_PRICE_KEY')
begin_price_key_dis = os.getenv('BEGIN_PRICE_KEY_DIS')
end_price_key = os.getenv('END_PRICE_KEY')


def parse_golden_apple(response):
    """Парсит цену на товар в GOLDEN APPLE."""
    try:
        soup = BeautifulSoup(response, 'lxml')
        try:
            dirt_name = soup.find('h1').text.split()
            name_thing = ' '.join(dirt_name)
            data = soup.find(tag_price_volume).find(tag_volume)
            raw_prices = data.find_next_sibling()
            raw_prices = raw_prices.text.split(key_price)

            first_price = int(raw_prices[0].strip().rstrip())
            second_price = int(re.sub(
                r"[^\d]",
                "",
                raw_prices[1].rstrip().rsplit('\n  ')[-1]
            ))
            prices = (first_price, second_price)
            green_price = min(prices)
            main_price = max(prices)

        except BaseException:
            dirt_name = soup.find('h1').text.split()
            name_thing = ' '.join(dirt_name)
            data = soup.find(tag_all_data, string=re.compile(key_all_data)).text
            begin_price_index = data.find(begin_price_key)
            if begin_price_index == -1:
                begin_price_index = data.find(begin_price_key_dis)
            end_price_index = data.find(end_price_key)
            prices = json.loads(
                '{'f'{data[begin_price_index:end_price_index]}''}}'
            )
            try:
                green_price = int(prices['price']['loyalty']['amount'])
            except BaseException:
                green_price = int(prices['price']['discount']['amount'])
            main_price = int(prices['price']['regular']['amount'])

        print(f'Название: {name_thing}')
        print(f'Цена с картой: {green_price}')
        print(f'Цена без карты: {main_price}')
        logger.info(f'Спарсены данные {name_thing, green_price}')
        return name_thing, green_price
    except BaseException as er:
        print(f'Возникла ошибка: {er}')

