from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.start_kb import *
from database.database import DataBase
from core.dictionary import *

router = Router(name=__name__)

@router.message(Command(commands='start'))
async def cmd_start(message: Message, bot: Bot):
    db = DataBase()
    if not await db.get_user(message.from_user.id):
        await db.add_user(
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.username,
            message.from_user.id
        )
    await bot.send_message(
        message.from_user.id,
        start_message,
        reply_markup=start_kb()
    )
    await message.delete()