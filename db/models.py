import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class ThingsTable(Base):
    __tablename__ = 'things'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    thing_name = Column(String)
    added_at = Column(DateTime, default=datetime.datetime.now)

    price = relationship(
        'PricesOfThingsTable',
        backref='thing',
        cascade='all, delete-orphan'
    )
    id_user = Column(Integer, ForeignKey('users.tg_id'))
    __table_args__ = (
        UniqueConstraint(
            'url', 'id_user', name='unique_url_user'
        ),
    )


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

    thing = relationship(
        'ThingsTable',
        backref='user'
    )
