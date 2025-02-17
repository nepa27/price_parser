import asyncio
import datetime

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

from models import Base, ThingsTable, PricesOfThingsTable, UsersTable

engine = create_async_engine('sqlite+aiosqlite:///example.db', echo=True)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_user(user_id: int):
    async with async_session() as session:
        response = select(UsersTable).where(
            UsersTable.tg_id == user_id,

        )
        result = await session.execute(response)
        user = result.scalar()

        if user:
            return user
        else:
            user = UsersTable(tg_id=user_id)
            session.add(user)
            await session.commit()


async def check_thing(url: str, user_id: int):
    async with async_session() as session:
        response = select(ThingsTable).where(
            and_(
                ThingsTable.url == url,
                ThingsTable.id_user == user_id,
            )
        )
        result = await session.execute(response)
        thing = result.scalar()

        return thing if thing else None


async def add_data_on_thing(url: str, user_id: int, data: list):
    async with async_session() as session:
        date_today = datetime.datetime.now()
        thing = ThingsTable(
            url=url,
            id_user=user_id,
            thing_name=data[0]
        )
        price = PricesOfThingsTable(
            price=data[1],
            id_thing=thing.id,
            added_at=date_today
        )
        session.add_all((thing, price))
        await session.commit()


async def add_new_price(thing_id: int, new_price: int):
    async with (async_session() as session):
        response = select(ThingsTable).where(ThingsTable.id == thing_id)
        result = await session.execute(response)
        thing = result.scalar()

        if thing:
            price = PricesOfThingsTable(price=new_price, thing=thing)
            session.add(price)
            await session.commit()
        else:
            print('Товара не существует!')


async def check_price():
    think_id = 1
    new_price = 100

    async with async_session() as session:
        response = select(PricesOfThingsTable).where(
            and_(
                PricesOfThingsTable.id_thing == think_id,
                PricesOfThingsTable.price == new_price
            )
        )
        result = await session.execute(response)
        price = result.scalar()

        return 'Цена не изменилась' if price else 'Цена изменилась'


async def get_list_things(user_id: int):
    async with async_session() as session:
        response = select(ThingsTable).where(
            ThingsTable.id_user == user_id,
        )
        result = await session.execute(response)
        data = result.scalars().all()
        return data if data else None
#
#
# async def main():
#     await init_db()  # Инициализация базы данных
#     # await add_data_on_thing()  # Добавление данных
#     # await check_price()
#     # await check_thing('http://example2.com', 1)
#     await get_list_things(123)
# # Запуск основной функции
# if __name__ == "__main__":
#     asyncio.run(main())
