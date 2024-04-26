from datetime import datetime
from aiogram.filters import Command
from aiogram import Router, types

from database.models import User, List, Task

user_router = Router()
DEFAULT_LIST_NAME = 'default'

@user_router.message(Command('start'))
async def cmd_start(message: types.Message) -> None:
    user = User.get(User.id == message.chat.id)
    if not User.select().where(User.id == message.chat.id):
        User.create(
            id=message.chat.id,
            date_of_registration=datetime.today()
        )

    if not List.select().where(List.name == DEFAULT_LIST_NAME):
        List.create(
            name = DEFAULT_LIST_NAME,
            date_of_creation = datetime.today(),
            user_id = user.id
        )
    await message.answer(
        f"Hi, {message.chat.first_name}!\n"
        "I'm <b>TaskTracker</b> - a Telegram bot for efficient task management!"
    )
    