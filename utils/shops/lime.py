from bs4 import BeautifulSoup


def parse_lime(response):
    """Парсит цену на товар в LIME."""
    soup = BeautifulSoup(response, 'lxml')
    # TODO: Проверить страницы со скидками, узнать название класса
    # green_price = soup.find('span', class_='s4m_27 ms3_27').text.rstrip(' ₽')
    main_price = soup.find(
        'div',
        class_='product__price'
    ).text.strip().rstrip(' руб. ')
    #
    # print(f'Цена по скидке: {green_price}')
    print(f'Цена: {main_price}')
