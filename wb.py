from bs4 import BeautifulSoup
import requests


def get_page():
    request = requests.get('http://192.168.1.133/wb/')

    soup = BeautifulSoup(request.text, 'lxml')
    green_price = soup.find('span', class_='product-line__price-wallet').text.strip().rstrip(' ₽  ')
    main_price = soup.find('b', class_='product-line__price-now wallet').text.strip().rstrip(' ₽  ')

    print(f'Цена с WB кошельком: {green_price}')
    print(f'Цена без WB кошелька: {main_price}')


get_page()
