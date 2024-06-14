from datetime import datetime

from aiogram import Bot
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from states.task_creation_state import CreateState
from utils.dictionary import *
from utils.logging_config import logger


async def handle_task_description_input(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Handles the input of the description for a new task.

    Args:
        message (Message): The message object containing the user's input.
        state (FSMContext): The state object for the conversation.

    Returns:
        None
    """
    await state.update_data(description_task=message.text)


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