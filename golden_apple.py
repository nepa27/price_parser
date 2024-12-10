from bs4 import BeautifulSoup
import requests


def get_page():
    request = requests.get('http://192.168.1.133/apple/')

    soup = BeautifulSoup(request.text, 'lxml')
    green_price = soup.find('div', class_='uLqLO baA1b').find('div').text.strip().rstrip('\n₽\n ')
    main_price = soup.find('div', class_='vTuTT _8denb').text.strip().rstrip('\n₽\n ')

    print(f'Цена с картой: {green_price}')
    print(f'Цена без карты: {main_price}')


get_page()
