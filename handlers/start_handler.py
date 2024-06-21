from venv import logger

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message

from database.database import DataBase
from keyboards.start_kb import *
from utils.dictionary import *


router = Router(name=__name__)

@router.message(Command(commands='start'))
async def handle_start_command(message: Message, bot: Bot):
    try:
        db = DataBase()
        if not await db.get_user(user_id=message.from_user.id):
            await db.add_user(
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                user_name=message.from_user.username,
                telegram_id=message.from_user.id
            )
        await bot.send_message(
            chat_id=message.from_user.id,
            text=start_message,
            reply_markup=start_kb()
        )
    except Exception as error:
        logger.error(f"Error in handle_start_command: {error}")
    finally:
        await message.delete()