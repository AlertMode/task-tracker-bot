from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from typing import Optional

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100))
    telegram_id: Mapped [str] = mapped_column(String(100))


class Tasks(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(Text)
    creation_date: Mapped[DateTime] = mapped_column(DateTime)
    update_date: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    completion_date: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))