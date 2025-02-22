import asyncio
import os

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from db.db import init_db, check_price
from handlers import questions

load_dotenv('.env')
TOKEN = os.environ.get('TELEGRAM_TOKEN')


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(questions.router)

    async def check_price_wrapper():
        await check_price(bot)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_price_wrapper, 'interval', hours=1)
    scheduler.start()

    await init_db()

    # TODO: Переделать на вебхук!
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
