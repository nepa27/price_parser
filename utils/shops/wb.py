from bs4 import BeautifulSoup


def parse_wb(response):
    """Парсит цену на товар и наличие размеров в WB."""
    soup = BeautifulSoup(response, 'lxml')

    list_sizes = soup.find(
        'ul', class_='sizes-list visible'
    ).find_all('label', class_='j-size sizes-list__button')
    green_price = soup.find(
        'span',
        class_='product-line__price-wallet'
    ).text.strip().rstrip(' ₽  ')
    main_price = soup.find(
        'b',
        class_='product-line__price-now wallet'
    ).text.strip().rstrip(' ₽  ')

    print(f'Цена с WB кошельком: {green_price}')
    print(f'Цена без WB кошелька: {main_price}')

    print('Наличие размеров:')
    for i, el in enumerate(list_sizes):
        size = el.find('span', class_='sizes-list__size').text
        print(f'{i + 1}. {size}')
