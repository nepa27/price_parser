import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv('.env')
key_price = os.getenv('FLAG_PRICE_GA')
tag_price_volume = os.getenv('TAG_PRICE_VOLUME_GA')
tag_volume = os.getenv('TAG_VOLUME_GA')


def parse_golden_apple(response):
    """Парсит цену на товар в GOLDEN APPLE."""

    soup = BeautifulSoup(response, 'lxml')
    data = soup.find(tag_price_volume).find(tag_volume)

    raw_prices = data.find_next_sibling()
    raw_prices = raw_prices.text.split(key_price)

    green_price = raw_prices[0].strip().rstrip()
    main_price = raw_prices[1].strip().rstrip()

    print(f'Цена с картой: {green_price}')
    print(f'Цена без карты: {main_price}')


with open('golden.html', 'r') as f:
    file = f.read()

parse_golden_apple(file)
