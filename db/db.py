import asyncio
import datetime
import os

from dotenv import load_dotenv
from sqlalchemy import event, select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

from db.models import Base, ThingsTable, PricesOfThingsTable, UsersTable
from log_config import logger
from utils.main import choose_shop

load_dotenv('.env')
ADMIN_ID = os.environ.get('ADMIN_ID')
engine = create_async_engine('sqlite+aiosqlite:///example.db', echo=False)


@event.listens_for(engine.sync_engine, 'before_cursor_execute')
def log_raw_queries(conn, cursor, statement, parameters, context, *args):
    if isinstance(statement, str) and 'FROM' in statement:
        logger.debug(f'Запрос в БД {statement} с параметрами {parameters}')


async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_user(user_id: int):
    try:
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
                logger.info(f'Пользователь с id = {user_id} добавлен в БД')
    except IntegrityError as e:
        logger.error(f'Попытка добавить существующего пользователя {e}')
        return None
    except SQLAlchemyError as e:
        logger.error(e)
        return None


async def check_thing(url: str, user_id: int):
    try:
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
    except SQLAlchemyError as e:
        logger.error(e)
        return None


async def add_data_on_thing(url: str, user_id: int, data: list):
    try:
        async with async_session() as session:
            thing_name, price = data
            date_today = datetime.datetime.now()
            thing = ThingsTable(
                url=url,
                id_user=user_id,
                thing_name=thing_name
            )
            session.add(thing)
            await session.flush()
            price = PricesOfThingsTable(
                price=price,
                id_thing=thing.id,
                added_at=date_today
            )
            session.add(price)
            await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(e)
        return None


async def add_new_price(new_price: int, id_thing: int):
    date_today = datetime.datetime.now()
    try:
        async with (async_session() as session):
            price = PricesOfThingsTable(
                price=new_price,
                id_thing=id_thing,
                added_at=date_today
            )
            session.add(price)
            await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(e)
        return None


async def get_list_things(user_id: int):
    try:
        async with async_session() as session:
            response = select(ThingsTable).where(
                ThingsTable.id_user == user_id,
            )
            result = await session.execute(response)
            data = result.scalars().all()
            return data if data else None
    except SQLAlchemyError as e:
        logger.error(e)
        return None


async def get_one_thing(think_id: int):
    try:
        async with async_session() as session:
            response = select(ThingsTable).where(
                ThingsTable.id == think_id,
            ).options(selectinload(ThingsTable.price))

            result = await session.execute(response)
            data = result.scalars().first()
            if data:
                latest_price = sorted(
                    data.price,
                    key=lambda price: price.added_at,
                    reverse=True
                )[0]
                data.latest_price = latest_price
            return data if data else None
    except SQLAlchemyError as e:
        logger.error(e)
        return None


async def delete_one_thing(think_id: int):
    try:
        async with async_session() as session:
            response = select(ThingsTable).where(
                ThingsTable.id == think_id,
            )
            result = await session.execute(response)
            thing = result.scalar()
            if thing:
                await session.delete(thing)
                await session.commit()
                return thing.thing_name
            else:
                return False
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(e)
        return None


async def check_price(bot):
    try:
        async with async_session() as session:
            response = select(ThingsTable).options(
                selectinload(ThingsTable.price)
            )
            result = await session.execute(response)
            things = result.scalars().all()

            for thing in things:
                thing_name, new_price = choose_shop(thing.url)
                old_price = thing.price.price

                if old_price != new_price:
                    await add_new_price(new_price, thing.id)
                    await bot.send_message(
                        chat_id=thing.id_user,
                        text=f'Цена на <b>{thing_name}</b> изменились!\n'
                             f'Старая цена: <b>{old_price}</b>\n'
                             f'Новая цена: <b>{new_price}</b>',
                        parse_mode='HTML'
                    )
                await bot.send_message(
                    chat_id=thing.id_user,
                    text=f'Цена на <b>{thing_name}</b> не изменились!\n'
                         f'Цена 3 часа назад: <b>{old_price}</b>\n'
                         f'Цена сейчас: <b>{new_price}</b>',
                    parse_mode='HTML'
                )

    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(e)
        return None
