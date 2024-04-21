import asyncio

from aiogram import Dispatcher

from bot_instance import bot
from handlers.user_handlers import user_router

def register_routers(dp: Dispatcher) -> None:
    """Register routers"""

    dp.include_router(user_router)

async def main() -> None:
    """Entry Point"""

    dp = Dispatcher()

    register_routers(dp)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())