import logging

from datetime import datetime
from aiogram.filters import Command
from aiogram import Router, types

from database.models import User, List, Task

user_router = Router()
DEFAULT_LIST_NAME = 'default'

@user_router.message(Command('start'))
async def cmd_start(message: types.Message) -> None:
    if not User.select().where(User.id == message.chat.id):
        User.create(
            id=message.chat.id,
            date_of_registration=datetime.today()
        )
    user = User.get(User.id == message.chat.id)

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

async def get_lists(user_id) -> list[str]:
    try:
        lists = List.select().where(List.user_id == user_id)

        response = []

        for list in lists:
            response.append(f"<b>{list.id}. {list.name}</b>\n")
    except Exception as e:
        logging.error(e)
        return []
    else:
        return "".join(response)
    