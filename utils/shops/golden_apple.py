from bs4 import BeautifulSoup
import requests


def parse_golden_apple(response):
    """Парсит цену на товар в GOLDEN APPLE."""

    soup = BeautifulSoup(response.text, 'lxml')
    green_price = soup.find(
        'div',
        class_='uLqLO baA1b'
    ).find('div').text.strip().rstrip('\n₽\n ')
    main_price = soup.find(
        'div',
        class_='vTuTT _8denb'
    ).text.strip().rstrip('\n₽\n ')

    print(f'Цена с картой: {green_price}')
