from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    Message
)

from database.database import DataBase
from keyboards.start_kb import *
from utils.dictionary import *
from utils.logging_config import logger


router = Router(name=__name__)


async def handle_start(
        user_id: int,
        user_first_name: str,
        user_last_name: str,
        username: str,
        state: FSMContext,
        bot: Bot
) -> None:
    """
    Sends the start message with the start keyboard to the user.

    Args:
        user_id (int): The ID of the user.
        user_first_name (str): The first name of the user.
        user_last_name (str): The last name of the user.
        username (str): The username of the user.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    try:
        db = DataBase()
        if not await db.get_user(user_id=user_id):
            await db.add_user(
                first_name=user_first_name,
                last_name=user_last_name,
                user_name=username,
                telegram_id=user_id
            )
        await bot.send_message(
            chat_id=user_id,
            text=start_message,
            reply_markup=start_kb()
        )
    except Exception as error:
        logger.error(f"handle_start: {error}")


@router.message(Command(commands='start'))
async def handle_start_command(message: Message, bot: Bot):
    """
    Handles the start command.

    Args:
        message (Message): The incoming message object.
        bot (Bot): The bot instance.
    
    Returns:
        None
    """
    try:
        await handle_start(
            user_id=message.from_user.id,
            user_first_name=message.from_user.first_name,
            user_last_name=message.from_user.last_name,
            username=message.from_user.username,
            bot=bot
        )
    except Exception as error:
        logger.error(f"in handle_start_command: {error}")
    finally:
        await message.delete()


@router.callback_query(
        MenuCommandsCallback.filter(
            F.option == MenuCommands.START
        )
)
async def handle_start_callback(
    callback: CallbackQuery,
    bot: Bot
) -> None:
    """
    Handles the start callback query.

    Args:
        callback (CallbackQuery): The callback query instance.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    await callback.answer()
    await handle_start(
        user_id=callback.from_user.id,
        user_first_name=callback.from_user.first_name,
        user_last_name=callback.from_user.last_name,
        username=callback.from_user.username,
        bot=bot
    )
    await callback.message.delete()
        