from datetime import datetime
import os

from sqlalchemy import (
    Sequence,
    delete,
    select,
    update
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from modules.list.task_list_callback import TaskStatus
from utils.logging_config import logger
from database.models import *


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
        """
        Creates database tables.

        Returns:
            None
        """
        try:
            async with self.async_engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)
        except SQLAlchemyError as error:
            logger.error(f'create_db() error: {error}')
            raise


    async def get_user(
            self,
            user_id: int
    ) -> Users:
        """
        Retrieves a user by user ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            Users: The user object if found, None otherwise.
        """
        try:
            async with self.Session() as session:
                result = await session.execute(
                    select(Users).where(Users.telegram_id == user_id)
                )
                return result.scalar()
        except SQLAlchemyError as error:
            logger.error(f'get_user() error: {error}')



    async def get_all_users(self) -> Sequence[Users]:
        """
        Retrieves all users from the database.

        Returns:
            Sequence[Users]: A sequence of all users in the database.
        """
        try:
            async with self.Session() as session:
                result = await session.execute(select(Users))
                return result.scalars().all()
        except SQLAlchemyError as error:
            logger.error(f'get_all_users() error: {error}')
            raise


    async def add_user(
            self,
            first_name: str,
            last_name: str,
            user_name: str,
            telegram_id: str
        ) -> None:
        """
        Add a new user to the database.

        Args:
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            user_name (str): The user's Telegram nickname.
            telegram_id (str): The user's Telegeram ID.

        Returns:
            None
        """
        try:
            async with self.Session() as session:
                session.add(
                    Users(
                        first_name=first_name,
                        last_name=last_name,
                        username=user_name,
                        telegram_id = telegram_id
                    )
                )
                await session.commit()
        except SQLAlchemyError as error:
            logger.error(f'add_user() error: {error}')
            await session.rollback()
            raise
    
    
    async def add_task(
            self,
            description: str,
            creation_date: datetime,
            user_id: int,
            reminder_date: Optional[datetime] = None
        ) -> None:
        """
        Add a new task to the database.

        Args:
            description (str): The description of the task.
            user_id (int): The ID of the user to whom the task belongs.
            creation_date (datetime): The creation date of the task.
            reminder_date (datetime, optional): The reminder date for the task. Defaults to None.
            recurring_days (List[RecurringDays], optional): The days of the week for the task's reminder. Defaults to None.

        Returns:
            None
        """   
        try:
            async with self.Session() as session:
                task = Tasks(
                    description=description,
                    creation_date=creation_date,
                    user_id=user_id,
                    reminder_date=reminder_date
                )
                session.add(task)
                await session.flush()

                await session.commit()
        except SQLAlchemyError as error:
            logger.error(f'add_tasks() error: {error}')
            await session.rollback()
            raise
    

    async def get_task_by_id(
            self,
            task_id: int
    ) -> Tasks:
        """
        Retrieve a single task based on its ID.
        """
        try:
            async with self.Session() as session:
                result = await session.execute(
                    select(Tasks).filter(Tasks.id == task_id)
                )
                return result.scalar()
        except SQLAlchemyError as error:
            logger.error(f'get_task_by_id() error: {error}')
            raise


    async def get_all_tasks_by_user(
            self,
            user_id: int,
            status: TaskStatus
        ) -> Sequence[Tasks]:
        """
        Retrieve tasks for a given user based on task status.

        Args:
            user_id (int): The ID of the user.
            status (TaskStatus): The status of tasks to retrieve (ONGOING or COMPLETED).

        Returns:
            Sequence[Tasks]: A sequence of tasks matching the specified status.
        """
        try:
            async with self.Session() as session:
                query = select(Tasks).filter(Tasks.user_id == user_id)
                if status == TaskStatus.COMPLETED:
                    query = query.filter(Tasks.completion_date.isnot(None))
                else:
                    query = query.filter(Tasks.completion_date.is_(None))

                result = await session.execute(query)
                return result.scalars().all()
        except SQLAlchemyError as error:
            logger.error(f'get_tasks() error: {error}')
            raise
        
    
    async def delete_task(
            self,
            user_id: int,
            task_id: int
    ) -> None:
        """
        Deletes a task from the database.

        Args:
            user_id (int): The ID of the user who owns the task.
            task_id (int): The ID of the task to delete.

        Returns:
            None
        """
        try:
            async with self.Session() as session:
                await session.execute(
                    delete(Tasks).where(
                        Tasks.user_id == user_id,
                        Tasks.id == task_id
                    )
                )
                await session.commit()
        except SQLAlchemyError as error:
            logger.error(f'delete_task() error: {error}')
            await session.rollback()
            raise


    async def set_task_done(
            self,
            user_id: int,
            task_id: int
    ) -> None:
        """
        Marks a task as completed.

        Args:
            user_id (int): The ID of the user who owns the task.
            task_id (int): The ID of the task to mark as completed.

        Returns:
            None
        """
        try:
            async with self.Session() as session:
                await session.execute(
                    update(Tasks)
                    .values(
                        completion_date=datetime.now()
                    )
                    .where(
                        Tasks.user_id == user_id,
                        Tasks.id == task_id
                    )
                )
                await session.commit()
        except SQLAlchemyError as error:
            logger.error(f'set_task_done() error: {error}')
            await session.rollback()
            raise


    async def set_task_undone(
            self,
            user_id: int,
            task_id: int
    ) -> None:
        """
        Marks a task as incomplete.

        Args:
            user_id (int): The ID of the user who owns the task.
            task_id (int): The ID of the task to mark as incomplete.

        Returns:
            None
        """
        try:
            async with self.Session() as session:
                await session.execute(
                    update(Tasks)
                    .values(
                        completion_date=None
                    )
                    .where(
                        Tasks.user_id == user_id,
                        Tasks.id == task_id
                    )
                )
                await session.commit()
        except SQLAlchemyError as error:
            logger.error(f'set_task_undone() error: {error}')
            await session.rollback()
            raise


    async def get_all_tasks_by_reminder_date(
            self,
            current_datetime: datetime
        ) -> Sequence[Tasks]:
        """
        Retrieve all tasks that have a reminder date equal to the current date.

        Args:
            current_datetime (datetime): The current date and time.

        Returns:
            Sequence[Tasks]: A sequence of tasks with a reminder date equal to the current date.
        """
        try:
            async with self.Session() as session:
                query = (
                    select(Tasks)
                    .filter(Tasks.reminder_date <= current_datetime)
                    .filter(Tasks.completion_date.is_(None))
                )
                result = await session.execute(query)
                return result.scalars().all()
        except SQLAlchemyError as error:
            logger.error(f'get_tasks_by_reminder_date() error: {error}')
            raise

    
    async def set_task_reminded(
            self,
            user_id: int,
            task_id: int
        ) -> None:
        """
        Marks a task as reminded.

        Args:
            user_id (int): The ID of the user who owns the task.
            task_id (int): The ID of the task to mark as reminded.

        Returns:
            None
        """
        try:
            async with self.Session() as session:
                await session.execute(
                    update(Tasks)
                    .values(
                        is_reminded=True
                    )
                    .where(
                        Tasks.user_id == user_id,
                        Tasks.id == task_id
                    )
                )
                await session.commit()
        except SQLAlchemyError as error:
            logger.error(f'set_task_reminded() error: {error}')
            await session.rollback()
            raise