import asyncio
import logging
from aiogram import Dispatcher

from core.menu import set_commands
from database.database import DataBase
from bot_instance import bot
from core.routers import router


async def start() -> None:  
    try:
        database = DataBase()
        await database.create_db()
        await set_commands(bot) 
        dp = Dispatcher()
        dp.include_router(router)
        await set_commands(bot)
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start())