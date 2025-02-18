import asyncio
import logging
from logging.handlers import RotatingFileHandler
import os
import sys

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from db.db import init_db
from handlers import questions


load_dotenv('.env')
TOKEN = os.environ.get('TELEGRAM_TOKEN')

log_format = (
    '%(asctime)s - [%(levelname)s] -  %(name)s - '
    '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(logging.Formatter(log_format))

file_handler = RotatingFileHandler(
    f'{__file__}.log',
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding='UTF-8',
)
file_handler.setFormatter(logging.Formatter(log_format))

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(questions.router)

    await init_db()

    # TODO: Переделать на вебхук!
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
