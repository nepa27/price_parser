import os
import time
from datetime import datetime

from fake_useragent import UserAgent
from selenium import webdriver

from constants import FILES_PATH


def get_page(url):
    html = None
    now_date = datetime.now().strftime('%d_%m_%Y|%H_%M_%S')
    user_agent = UserAgent().random

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(3)

        html = driver.page_source

        if not os.path.exists(FILES_PATH):
            os.mkdir(FILES_PATH)

        with open(f'{FILES_PATH}/{now_date}.html', 'w') as file:
            file.write(html)
    except BaseException as er:
        print(f'Возникла ошибка: {er}')
    finally:
        driver.quit()

    return html
