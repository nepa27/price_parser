import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from db.db import init_db
from handlers import questions


load_dotenv('.env')
TOKEN = os.environ.get('TELEGRAM_TOKEN')


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
