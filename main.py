import asyncio
import logging

from aiogram import Dispatcher

from utils.menu import set_menu
from database.database import DataBase
from bot_instance import bot
from utils.routers import router


async def main() -> None:  
    try:
        database = DataBase()
        await database.create_db()

        await set_menu(bot)

        dp = Dispatcher()
        dp.include_router(router)

        await set_menu(bot)
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())