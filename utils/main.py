from utils.shops import golden_apple, lime, wb, ozon
from utils.request import get_page, get_page_ozon


async def choose_shop(url):
    if 'ozon' in url:
        data = get_page_ozon(url)
        return ozon.parse_ozon(data)
    else:
        data = get_page(url)
        if 'wb' in url or 'wildberries' in url:
            return wb.parse_wb(data)
        elif 'goldapple' in url:
            return golden_apple.parse_golden_apple(data)
        elif 'lime-shop' in url:
            return lime.parse_lime(data)
        else:
            return None
