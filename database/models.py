from typing import List, Optional
from sqlalchemy import (
    Boolean, DateTime, Integer, ForeignKey,
    String, Text, UniqueConstraint
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column,
    relationship
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from enum import Enum


class Base(AsyncAttrs, DeclarativeBase):
    pass


class DaysOfWeek(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100))
    telegram_id: Mapped[str] = mapped_column(String(100))
    tasks: Mapped[List["Tasks"]] = relationship("Tasks", back_populates="user")


class Tasks(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(Text)
    creation_date: Mapped[DateTime] = mapped_column(DateTime)
    update_date: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    reminder_date: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    completion_date: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    is_recurrent: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user: Mapped["Users"] = relationship("Users", back_populates="tasks")
    days_of_week: Mapped[List["DaysOfWeek"]] = relationship("DaysOfWeek", back_populates="task")


class DaysOfWeek(Base):
    __tablename__ = 'days_of_week'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    day: Mapped[DaysOfWeek] = mapped_column(Integer)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey('tasks.id'))
    task: Mapped["Tasks"] = relationship("Tasks", back_populates="days_of_week")

    __table_args__ = (
        UniqueConstraint('task_id', 'day', name='unique_task_day'),
    )
