import datetime
import os

from enum import IntEnum, auto
from sqlalchemy import Sequence, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import *


class TaskStatus(IntEnum):
    ONGOING = auto()
    COMPLETED = auto()


class DataBase():
    def __init__(self):
        self.db_host = os.getenv('DB_HOST')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_name = os.getenv('DB_NAME')
        self.connect = f'mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}?charset=utf8mb4'
        self.async_engine = create_async_engine(self.connect)
        self.Session = async_sessionmaker(bind=self.async_engine, class_=AsyncSession)


    async def create_db(self) -> None:
        async with self.async_engine.begin() as connect:
            await connect.run_sync(Base.metadata.create_all)


    async def get_user(self, user_id) -> Users:
        async with self.Session() as request:
            result = await request.execute(
                select(Users).where(Users.telegram_id == user_id)
            )
        return result.scalar()
    

    async def add_user(self, first_name, last_name, user_name, telegram_id) -> None:
        async with self.Session() as request:
            request.add(
                Users(
                    first_name=first_name,
                    last_name=last_name,
                    username=user_name,
                    telegram_id = telegram_id
                )
            )
            await request.commit()


    async def get_table(self, table_name):
        async with self.Session() as request:
            result = await request.execute(select(table_name))
        return result.scalars().all()
    
    
    async def add_task(self, description, creation_date, user_id) -> None:
        async with self.Session() as request:
            request.add(
                Tasks(
                    description=description,
                    creation_date=creation_date,
                    user_id=user_id
                )
            )
            await request.commit()
    

    async def get_tasks(self, user_id: int, status: TaskStatus) -> Sequence[Tasks]:
        """
            Retrieve tasks for a given user based on task status.

            Args:
                user_id (int): The ID of the user.
                status (TaskStatus): The status of tasks to retrieve (ONGOING or COMPLETED).

            Returns:
                Sequence[Tasks]: A sequence of tasks matching the specified status.
        """
        async with self.Session() as request:
            try:
                result = await request.execute(
                    select(Tasks).filter(
                        Tasks.user_id == user_id,
                        Tasks.completion_date.isnot(None) 
                            if status == TaskStatus.COMPLETED
                            else Tasks.completion_date == None
                    )
                )
            except Exception as error:
                print(f'get_tasks() error: {error}')
            finally:
                return result.scalars().all()
        
    
    async def delete_task(self, user_id, task_id) -> None:
        async with self.Session() as request:
            await request.execute(
                delete(Tasks).where(
                    Tasks.user_id == user_id,
                    Tasks.id == task_id
                )
            )
            await request.commit()


    async def set_task_done(self, user_id, task_id) -> None:
        async with self.Session() as request:
            await request.execute(
                update(Tasks)
                .values(
                    completion_date=datetime.datetime.now()
                )
                .where(
                    Tasks.user_id == user_id,
                    Tasks.id == task_id
                )
            )
            await request.commit()


    async def set_task_undone(self, user_id, task_id) -> None:
        async with self.Session() as request:
            await request.execute(
                update(Tasks)
                .values(
                    completion_date=None
                )
                .where(
                    Tasks.user_id == user_id,
                    Tasks.id == task_id
                )
            )
            await request.commit()