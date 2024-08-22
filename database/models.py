from enum import StrEnum
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


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Days_of_Week(StrEnum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


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
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user: Mapped["Users"] = relationship("Users", back_populates="tasks")
    recurring_days: Mapped[List["RecurringDays"]] = relationship("RecurringDays", back_populates="task")


class RecurringDays(Base):
    __tablename__ = 'recurring_days'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    day: Mapped[Days_of_Week] = mapped_column(String(10))
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey('tasks.id'))
    task: Mapped["Tasks"] = relationship("Tasks", back_populates="recurring_days")

    __table_args__ = (
        UniqueConstraint('task_id', 'day', name='unique_task_day'),
    )
