from datetime import datetime

import asyncio

from aiogram import Bot
import aioschedule as shcedule
from sqlalchemy import Sequence

from database.database import *
from modules.list.task_list_callback import *
from modules.alter.task_alteration_kb import *
from utils.dictionary import *
from utils.logging_config import logger


async def send_reminder(bot: Bot, task: Tasks, user_id: str) -> None:
    """
    Sends a reminder to the user about the task.
    Allows the user to mark the task as done or delete the task.
    
    Args:
        bot (Bot): The bot instance.
        task (Task): The task to remind the user about.

    Returns:
        None
    """
    try:
        await bot.send_message(
            chat_id=user_id,
            text = (
                task_ongoing % (
                    task.creation_date,
                    task.description,
                    task.reminder_date
                )),
            reply_markup=task_ongoing_kb(task.id)
        )
      
    except Exception as error:
        logger.error(f"send_reminder: {error}")


async def check_reminders(bot: Bot, database: DataBase) -> None:
    """
    Checks the reminders and sends the reminders to the users.
    
    Args:
        bot (Bot): The bot instance.
        db (DataBase): The database instance.
    
    Returns:
        None
    """
    try:
        start_of_minute = datetime.now().replace(second=0, microsecond=0)
        users = await database.get_all_users()

        for user in users:
            tasks = await database.get_all_tasks_by_user(
                user_id=user.id,
                status=TaskStatus.ONGOING
            )

            for task in tasks:
                if (
                    task.reminder_date 
                    and task.reminder_date <= start_of_minute
                    and task.is_reminded is False
                    ):
                    await send_reminder(bot=bot, task=task, user_id=user.telegram_id)
                    await database.set_task_reminded(
                        user_id=user.id,
                        task_id=task.id
                    )

    except Exception as error:
        logger.error(f"check_reminders: {error}")
        

async def run_scheduler(bot: Bot, database: DataBase) -> None:
    """
    Runs the scheduler to check the reminders.
    
    Args:
        bot (Bot): The bot instance.
        database (DataBase): The database instance.
    
    Returns:
        None
    """
    try:
        while True:
            await check_reminders(bot=bot, database=database)
            await asyncio.sleep(60)
    
    except Exception as error:
        logger.error(f"run_scheduler: {error}")
