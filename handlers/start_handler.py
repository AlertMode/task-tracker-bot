from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.start_kb import *
from database.database import DataBase
from utils.dictionary import *

router = Router(name=__name__)

@router.message(Command(commands='start'))
async def cmd_start(message: Message, bot: Bot):
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
    await message.delete()