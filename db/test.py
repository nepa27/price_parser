import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from models import Base, ThingsTable, PricesOfThingsTable, UsersTable

engine = create_async_engine('sqlite+aiosqlite:///example.db', echo=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_data():
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        user = UsersTable(tg_id=123456, username='Test')
        thing = ThingsTable(url='http://example2.com', id_user=1)
        price = PricesOfThingsTable(price=99, thing=thing)
        session.add_all((user, thing, price))
        await session.commit()


async def main():
    await init_db()  # Инициализация базы данных
    await add_data()  # Добавление данных


# Запуск основной функции
if __name__ == "__main__":
    asyncio.run(main())
