from typing import List, Optional
from sqlalchemy import (
    Boolean, DateTime, Integer, ForeignKey,
    String, Text
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column,
    relationship
)
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


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
    reminder_utc: Mapped[Optional[str]] = mapped_column(String(100))
    completion_date: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    is_reminded: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user: Mapped["Users"] = relationship("Users", back_populates="tasks")

