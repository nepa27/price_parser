from bs4 import BeautifulSoup
import requests


def get_page():
    request = requests.get('http://192.168.1.133/wb/')

    return request


def parse_price(request):
    soup = BeautifulSoup(request.text, 'lxml')
    green_price = soup.find('span', class_='product-line__price-wallet').text.strip().rstrip(' ₽  ')
    main_price = soup.find('b', class_='product-line__price-now wallet').text.strip().rstrip(' ₽  ')

    print(f'Цена с WB кошельком: {green_price}')
    print(f'Цена без WB кошелька: {main_price}')


def parse_size(request):
    soup = BeautifulSoup(request.text, 'lxml')
    list_sizes = soup.find(
        'ul', class_='sizes-list visible'
    ).find_all('label', class_='j-size sizes-list__button')

    print('Наличие размеров:')
    for i, el in enumerate(list_sizes):
        size = el.find('span', class_='sizes-list__size').text
        print(f'{i + 1}. {size}')


req = get_page()

parse_price(req)
parse_size(req)
