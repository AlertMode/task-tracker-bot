import asyncio
import logging
from aiogram import Dispatcher

from core.menu import set_commands
from database.database import DataBase
from bot_instance import bot
from handlers.start.start import start_router
from handlers.create_task.create_task import create_task_router


def register_routers(dp: Dispatcher) -> None:
    """Register routers"""
    dp.include_router(start_router)
    dp.include_router(create_task_router)


async def start() -> None:
    """Entry Point"""
    try:
        database = DataBase()
        await database.create_db()
        await set_commands(bot) 
        dp = Dispatcher()
        register_routers(dp)
        await set_commands(bot)
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start())