import asyncio
import logging

from aiogram import Dispatcher

from bot_instance import bot
from database.database import DataBase
from scheduler_handler import run_scheduler
from routers.routers import router
from utils.menu import set_menu


async def main() -> None:  
    try:
        database = DataBase()
        await database.create_db()

        await set_menu(bot)

        dp = Dispatcher()
        dp.include_router(router)

        asyncio.create_task(run_scheduler(bot, database))

        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())