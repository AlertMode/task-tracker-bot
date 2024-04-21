from aiogram.filters import Command
from aiogram import Router, types


user_router = Router()

greeting_message = (
    'Hello! I\'m TaskTracker - a Telegram bot for efficient task management. '
    'Add, list, mark, and remove tasks with ease. '
    'Set reminders and manage custom lists.'
)

@user_router.message(Command('start'))
async def cmd_start(msg: types.Message) -> None:
    """Processes the `start` command

    Args:
        msg (types.Message): a message from user
    """
    await msg.answer(greeting_message)