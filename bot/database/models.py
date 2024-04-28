from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100))
    telegram_id: Mapped [str] = mapped_column(String(100), nullable=False)

    list: Mapped[list['Lists']] = relationship( # type: ignore
        'Lists',
        back_populates='user',
        cascade='all, delete'
    )

class Lists(Base):
    __tablename__ = 'lists'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    creation_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    update_date: Mapped[DateTime] = mapped_column(DateTime)
    completion_date: Mapped[DateTime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    
    user: Mapped[Users] = relationship('Users', foreign_keys='Lists.user_id')
    task: Mapped[list['Tasks']] = relationship( # type: ignore
        'Tasks',
        back_populates='list',
        cascade='all, delete'
    )
    
class Tasks(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    creation_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    update_date: Mapped[DateTime] = mapped_column(DateTime)
    completion_date: Mapped[DateTime] = mapped_column(DateTime)
    list_id: Mapped[int] = mapped_column(Integer, ForeignKey('lists.id'))

    list: Mapped[Lists] = relationship('Lists', foreign_keys='Tasks.list_id') # type: ignore