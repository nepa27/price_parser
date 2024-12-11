from bs4 import BeautifulSoup


def parse_ozon(response):
    """Парсит цену на товар в OZON."""
    soup = BeautifulSoup(response.text, 'lxml')
    green_price = soup.find(
        'span',
        class_='s4m_27 ms3_27'
    ).text.rstrip(' ₽')
    main_price = soup.find(
        'span',
        class_='sm9_27 s9m_27 mt3_27'
    ).text.rstrip(' ₽')

    print(f'Цена с Озон картой: {green_price}')
    print(f'Цена без Озон картой: {main_price}')
