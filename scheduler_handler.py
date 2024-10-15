from datetime import datetime

import asyncio

from aiogram import Bot
import aioschedule as shcedule

from bot_instance import TOKEN
from database.database import DataBase
from utils.logging_config import logger


bot = Bot(token=TOKEN)
db = DataBase()


async def check_reminders(bot: Bot, db: DataBase) -> None:
    """
    Checks the reminders and sends the reminders to the users.
    
    Args:
        bot (Bot): The bot instance.
        db (DataBase): The database instance.
    
    Returns:
        None
    """
    try:
        #TODO: Finish the implementation.
        pass
    except Exception as error:
        logger.error(f"check_reminders: {error}")
        
    

        