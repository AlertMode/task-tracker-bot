import asyncio

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from token_api import TOKEN_API

dp = Dispatcher()

greeting_message = (
    'Hello! I\'m TaskTracker - a Telegram bot for efficient task management. '
    'Add, list, mark, and remove tasks with ease. '
    'Set reminders and manage custom lists.'
)

@dp.message(CommandStart())
async def cmd_start(msg: types.Message) -> None:
    await msg.answer(
        text=greeting_message
    )

async def main() -> None:
    bot = Bot(TOKEN_API)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())