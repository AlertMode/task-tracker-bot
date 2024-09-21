from datetime import datetime

import asyncio
import aioschedule as scheduler
from aiogram import Bot

from database.database import DataBase
from modules.list.task_list_callback import TaskStatus
from utils.logging_config import logger


user_ids = set()  # Global set to track users with scheduling tasks


async def job(
   user_id: int,
   bot: Bot
):
    try:
        db = DataBase()
        tasks = await db.get_all_tasks_by_user(
            user_id=user_id,
            status=TaskStatus.ONGOING
        )

        if(tasks):
            for task in tasks:
                if task.reminder_date:
                    print('reminder_date: ', task.reminder_date)
                    print('today: ', datetime.today())
                    if (task.reminder_date.replace(microsecond=0) == 
                        datetime.today().replace(microsecond=0)):
                        await bot.send_message(
                            chat_id=user_id,
                            text=f"Reminder: {task.description}"
                        ) 
    except Exception as error:
        logger.error(f"job: {error}")
        raise error
    

async def start_user_job(user_id: int, bot: Bot):
    try:
        if user_id not in user_ids:
            user_ids.add(user_id)
            scheduler.every(1).minutes.do(
                lambda: asyncio.create_task(job(user_id=user_id, bot=bot))
            )
    except Exception as error:
        logger.error(f"start_user_job: {error}")
        raise error