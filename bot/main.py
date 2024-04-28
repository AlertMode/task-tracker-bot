import asyncio
import logging
from aiogram import Dispatcher
from utlis.commands import set_commands
from database.database import DataBase
from bot_instance import bot
from handlers.start.start import start_router

def register_routers(dp: Dispatcher) -> None:
    """Register routers"""
    dp.include_router(start_router)

async def start() -> None:
    """Entry Point"""
    await set_commands(bot) 
    try:
        database = DataBase()
        await database.create_db()
        dp = Dispatcher()
        register_routers(dp)
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start())