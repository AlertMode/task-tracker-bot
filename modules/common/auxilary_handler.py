import re

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from utils.logging_config import logger


async def store_message_id(state: FSMContext, message_id: int) -> None:
    """
    Stores the message ID in the state.

    Args:
        state (FSMContext): The state of the conversation.
        message_id (int): The message ID.

    Returns:
        None
    """
    try:
        data = await state.get_data()
        messages = data.get('messages', [])
        messages.append(message_id)
        await state.update_data(messages=messages)
    except Exception as error:
        logger.error(f'store_message_id(): {error}')


async def get_stored_message_ids(state: FSMContext) -> list[int]:
    """
    Retrieves the stored message IDs from the state.

    Args:
        state (FSMContext): The state of the conversation.

    Returns:
        list[int]: The list of message IDs.
    """
    try:
        data = await state.get_data()
        return data.get('messages', [])
    except Exception as error:
        logger.error(f'Error: get_stored_message_ids(): {error}')
        return []


async def delete_all_messages(state: FSMContext, bot: Bot, chat_id: int) -> None:
    """
    Deletes all the messages in the conversation.

    Args:
        state (FSMContext): The state of the conversation.
        bot (Bot): The bot instance.
        chat_id (int): The chat ID.

    Returns:
        None
    """
    try:
        message_ids = await get_stored_message_ids(state=state)
        for message_id in message_ids:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
        
        await state.update_data(messages=[])
    except Exception as error:
        logger.error(f'Error: delete_all_messages(): {error}')


def valid_reminder_time(time: str) -> str | None:
    """
    Validates the reminder time input.

    Args:
        time (str): The reminder time input.

    Returns:
        str | None: The reminder time if valid, otherwise None.
    """
    try:
        pattern = r"^\d{2}:\d{2}(?: [+-]\d{1,2})?$"
        if re.match(pattern, time):
            return time
    except Exception as error:
        logger.error(f'Error: valid_reminder_time(): {error}')
        return None
    
