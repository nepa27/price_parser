import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class ThingsTable(Base):
    __tablename__ = 'things'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    added_at = Column(DateTime, default=datetime.datetime.now)

    price = relationship(
        'PricesOfThingsTable',
        backref='thing'
    )
    id_user = Column(Integer, ForeignKey('users.id'))


class PricesOfThingsTable(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    added_at = Column(DateTime, default=datetime.datetime.now)

    id_thing = Column(Integer, ForeignKey('things.id'))


class UsersTable(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    username = Column(String)

    thing = relationship(
        'ThingsTable',
        backref='user'
    )
