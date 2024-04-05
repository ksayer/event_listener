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

    @classmethod
    def filter_by_created(cls, created: datetime):
        stmt = select(cls).filter(cls.created > created)
        return session.execute(stmt).scalars().all()


class EventDaemon(Base, MethodManager):
    __tablename__ = 'EventDaemon'
    id: Mapped[int] = mapped_column(primary_key=True)
    last_checked_block: Mapped[int]

    @classmethod
    def get_or_create(cls, current_block: int) -> 'EventDaemon':
        return (
            session.execute(select(cls)).scalar_one_or_none()
            or
            cls.create(last_checked_block=current_block - (24 * 60 * 6))
        )

    @classmethod
    def update_block(cls, number: int):
        stmt = update(cls).values(last_checked_block=number)
        session.execute(stmt)
        session.commit()


class NotificationDaemon(Base, MethodManager):
    __tablename__ = 'NotificationDaemon'
    id: Mapped[int] = mapped_column(primary_key=True)
    last_report_at = mapped_column(DateTime(timezone=True), nullable=True)

    @classmethod
    def get_or_create(cls) -> 'NotificationDaemon':
        return session.execute(select(cls)).scalar_one_or_none() or cls.create()

    @classmethod
    def update_time(cls):
        stmt = update(cls).values(last_report_at=datetime.now())
        session.execute(stmt)
        session.commit()
