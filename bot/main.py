import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Dispatcher

from bot_instance import bot
from handlers.user_handlers import user_router
from utlis.commands import set_commands

def register_routers(dp: Dispatcher) -> None:
    """Register routers"""

    dp.include_router(user_router)

async def start() -> None:
    """Entry Point"""
    await set_commands(bot)
    try:
        dp = Dispatcher()
        register_routers(dp)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start())