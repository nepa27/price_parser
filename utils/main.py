from utils.shops import golden_apple, lime, wb
from utils.request import get_page


async def choose_shop(url):
    data = get_page(url)
    if 'wb' in url or 'wildberries' in url:
        return wb.parse_wb(data)
    elif 'goldapple' in url:
        return golden_apple.parse_golden_apple(data)
    elif 'lime-shop' in url:
        return lime.parse_lime(data)
    else:
        return None
