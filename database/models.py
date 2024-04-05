from datetime import datetime

from sqlalchemy import DateTime, func, DECIMAL, select, update
from sqlalchemy.orm import Mapped, mapped_column

from database.db import Base, session


class MethodManager:
    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        return obj


class TotalDistribution(Base, MethodManager):
    __tablename__ = 'TotalDistribution'

    id: Mapped[int] = mapped_column(primary_key=True)

    aix_processed = mapped_column(DECIMAL(precision=100, scale=0), default=0, server_default='0')
    aix_distributed = mapped_column(DECIMAL(precision=100, scale=0), default=0, server_default='0')
    eth_bought = mapped_column(DECIMAL(precision=100, scale=0), default=0, server_default='0')
    eth_distributed = mapped_column(DECIMAL(precision=100, scale=0), default=0, server_default='0')

    created = mapped_column(
        DateTime(timezone=True), default=datetime.now, server_default=func.now()
    )


class EventDaemon(Base, MethodManager):
    __tablename__ = 'EventDaemon'
    id: Mapped[int] = mapped_column(primary_key=True)
    last_checked_block: Mapped[int]

    @classmethod
    def get(cls) -> 'EventDaemon':
        return session.execute(select(cls)).scalar_one_or_none()

    @classmethod
    def update_block(cls, number: int):
        stmt = update(cls).values(last_checked_block=number)
        session.execute(stmt)
        session.commit()
