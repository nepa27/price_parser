from bs4 import BeautifulSoup
import requests


def get_page():
    request = requests.get('http://192.168.1.133/ozon/')

    soup = BeautifulSoup(request.text, 'lxml')
    green_price = soup.find('span', class_='s4m_27 ms3_27').text.rstrip(' ₽')
    main_price = soup.find('span', class_='sm9_27 s9m_27 mt3_27').text.rstrip(' ₽')

    print(f'Цена с Озон картой: {green_price}')
    print(f'Цена без Озон картой: {main_price}')


get_page()
