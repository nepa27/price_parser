from datetime import datetime
import os

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests

from constants import FILES_PATH

def get_page(url):
    now_date = datetime.now().strftime('%d_%m_%Y|%H_%M_%S')
    user_agent = UserAgent().random
    headers = {
        'user-agent': user_agent
    }
    request = requests.get(
        url,
        headers=headers
    )

    if not os.path.exists(FILES_PATH):
        os.mkdir(FILES_PATH)

    with open(f'{FILES_PATH}/{now_date}.html', 'w') as file:
        file.write(request.text)

    return request

def parse_price(request):
    soup = BeautifulSoup(request.text, 'lxml')
    # TODO: Проверить страницы со скидками, узнать название класса
    # green_price = soup.find('span', class_='s4m_27 ms3_27').text.rstrip(' ₽')
    main_price = soup.find('div', class_='product__price').text.strip().rstrip(' руб. ')
    #
    # print(f'Цена по скидке: {green_price}')
    print(f'Цена: {main_price}')


req = get_page('https://lime-shop.com/ru_ru/product/21901_9983_688-sero_koricnevyi')

#parse_price(req)