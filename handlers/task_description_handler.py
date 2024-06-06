from datetime import datetime

from aiogram import Bot
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from database.database import DataBase
from utils.dictionary import *
from utils.logging_config import logger


async def handle_task_description_input(
    message: Message,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    Handles the input of the description for a new task.

    Args:
        message (Message): The message object containing the user's input.
        state (FSMContext): The state object for the conversation.
        bot (Bot): The bot object for sending messages.

    Returns:
        None
    """
    await state.update_data(description_task=message.text)
    
    task = await state.get_data()
    try:
        db = DataBase()
        user = await db.get_user(message.from_user.id)
        await db.add_task(
            description=task['description_task'],
            creation_date=datetime.today(),
            user_id=user.id
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text=task_creation_completed,
            reply_markup=None
        )
    except Exception as error:
        logger.error(f'Error: handle_task_description_input: {error}')
        await bot.send_message(
            chat_id=message.from_user.id,
            text=error_message,
            reply_markup=None
        )
    finally:
        await state.clear()


async def handle_invalid_description_content_type(message: Message, bot: Bot) -> None:
    """
    Handler function for handling invalid content type when inputting description for a task.

    Args:
        message (Message): The incoming message object.
        bot (Bot): The bot object used to send messages.

    Returns:
        None
    """
    await bot.send_message(
        chat_id=message.from_user.id,
        text=task_createion_invalid_content_type,
        reply_markup=None
    )