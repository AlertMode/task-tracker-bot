from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from modules.add.task_creation_state import CreateState
from modules.common.auxilary_handler import *
from utils.dictionary import *


router = Router(name=__name__)


@router.message(
        CreateState.reminder_time,
        F.text.cast(validate_time_format).as_("time")
)
async def handle_reminder_time_input(
    message: Message,
    time: datetime,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    Handles the selection of the time for a recurring reminder.

    Args:
        message (Message): The incoming message object.
        time (datetime): The selected time.
        state (FSMContext): The state of the conversation.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    try:
        #TODO: Implement the time selection.
        #TODO: Add ReplyKeyboard to cancel the operation.
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'Time: {time}',
            reply_markup=None
        )
        print(f'Time: {time}')
    except Exception as error:
        logger.error(f"handle_reminder_time_input: {error}")


@router.message(
    CreateState.reminder_time,
)
async def handle_reminder_invalid_time_input(
    message: Message,
    bot: Bot
) -> None:
    """
    Handles the invalid time input for the reminder.

    Args:
        message (Message): The incoming message object.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    #TODO: Create a warning handelr!S
    try:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'ERROR: {message.text}',
            reply_markup=None
        )
    except Exception as error:
        logger.error(f"handle_reminder_invalid_time_input: {error}")