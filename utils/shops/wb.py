import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from utils.request import get_page

load_dotenv('.env')
key_price = os.getenv('FLAG_PRICE_WB')
tag_price = os.getenv('TAG_PRICE_WB')
tag_list_size = os.getenv('TAG_LIST_SIZE_WB')
class_list_size = os.getenv('CLASS_LIST_SIZE_WB')
tag_size = os.getenv('TAG_SIZE_WB')
class_size = os.getenv('CLASS_SIZE_WB')


def parse_wb(response):
    """Парсит цену на товар и наличие размеров в WB."""
    soup = BeautifulSoup(response, 'lxml')

    try:
        dirt_name = soup.find('h1').text.split()
        name_thing = ' '.join(dirt_name)
        list_sizes = soup.find_all(
            tag_list_size, class_=class_list_size)

        for tag in soup.find_all(tag_price):
            if key_price in tag.get_text():
                prices = tag.get_text()
                break
        prices = prices.split(key_price)
        green_price = prices[0].strip()
        main_price = prices[1].strip()

        print(f'Название: {name_thing}')
        print(f'Цена с WB кошельком: {green_price}')
        print(f'Цена без WB кошелька: {main_price}')

        print('Наличие размеров:')
        for i, el in enumerate(list_sizes):
            size = el.find(tag_size, class_=class_size).text
            print(f'{i + 1}. {size}')
    except BaseException as er:
        print(f'Возникла ошибка: {er}')


with open('wb.html', 'r') as f:
    file = f.read()
parse_wb(file)
# parse_wb(get_page('https://www.wildberries.ru/catalog/15398363/detail.aspx'))
