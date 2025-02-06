import asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

from models import Base, ThingsTable, PricesOfThingsTable, UsersTable

engine = create_async_engine('sqlite+aiosqlite:///example.db', echo=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Срабатывает когда пользователь нажимает /start и запускает бота
async def add_user():
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        user = UsersTable(tg_id=123456, username='Test')
        session.add(user)
        await session.commit()


async def check_thing():
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        thing = await session.get(ThingsTable, 2)
        if thing:
            return 'Товар уже отслеживается!'
        else:
            return 'Товар не существует! Нужно добавить!'


async def add_data_on_thing():
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        thing = ThingsTable(url='http://example2.com', id_user=1)
        price = PricesOfThingsTable(price=99, thing=thing)
        session.add_all((thing, price))
        await session.commit()


async def add_new_price():
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        thing = await session.get(ThingsTable, 2)
        if thing:
            price = PricesOfThingsTable(price=92, thing=thing)
            session.add(price)
            await session.commit()
        else:
            print('Товара не существует!')


async def check_price():
    think_id = 1
    new_price = 100

    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        thing = await session.query(PricesOfThingsTable).where(
            PricesOfThingsTable.id_thing == think_id,
            PricesOfThingsTable.price == new_price
        )
        if thing:
            return 'Цена не изменилась'
        else:
            return 'Цена изменилась'


async def main():
    await init_db()  # Инициализация базы данных
    # await add_data()  # Добавление данных
    await add_new_price()


# Запуск основной функции
if __name__ == "__main__":
    asyncio.run(main())
