from msilib import make_id
from sqlalchemy import select, delete, not_
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from database.models import *
import os

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


    async def get_user(self, user_id):
        async with self.Session() as request:
            result = await request.execute(
                select(Users).where(Users.telegram_id == user_id)
            )
        return result.scalar()
    

    async def add_user(self, first_name, last_name, user_name, telegram_id):
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
    
    
    async def add_task(self, description, creation_date, user_id):
        async with self.Session() as request:
            request.add(
                Tasks(
                    description=description,
                    creation_date=creation_date,
                    user_id=user_id
                )
            )
            await request.commit()
    

    async def get_tasks(self, areCompleted):
        async with self.Session() as request:
            result = await request.execute(
                select(Tasks).filter(
                    Tasks.completion_date.isnot(None) if areCompleted else Tasks.completion_date == None
                )
            )
            return result.scalars().all()