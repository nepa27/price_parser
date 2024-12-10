from bs4 import BeautifulSoup
import requests


def get_page():
    request = requests.get('http://192.168.1.133/lime/')

    soup = BeautifulSoup(request.text, 'lxml')
    # TODO: Проверить страницы со скидками, узнать название класса
    # green_price = soup.find('span', class_='s4m_27 ms3_27').text.rstrip(' ₽')
    main_price = soup.find('div', class_='product__price').text.split()[0].rstrip(' руб. ')
    #
    # print(f'Цена с Озон картой: {green_price}')
    print(f'Цена: {main_price}')


get_page()
