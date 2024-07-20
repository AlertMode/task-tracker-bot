from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from modules.add.task_creation_state import CreateState
from modules.common.auxilary_handler import *
from modules.set.reminder_recurring_kb import *
from utils.dictionary import *


router = Router(name=__name__)


@router.message(
        CreateState.reminder_time,
        F.text.cast(validate_time_format).as_("time")
)
async def handle_reminder_time_input(
    message: Message,
    time: time,
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
    #TODO: Figure out how to delete the instrucion messages.
    try:
        await state.update_data(reminder_time=time)
        await state.set_state(CreateState.reminder_interval)
        await store_message_id(
            state=state,
            message_id=message.message_id
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text=task_reminder_interval_selection,
            reply_markup=reminder_interval_selection_kb()
        )
        await message.delete()

        print(f'Time: {time}')
    except Exception as error:
        logger.error(f"handle_reminder_time_input: {error}")


@router.message(
    CreateState.reminder_time,
)
async def handle_reminder_invalid_time_input(
    message: Message,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    Handles the invalid time input for the reminder.

    Args:
        message (Message): The incoming message object.
        state (FSMContext): The state of the conversation.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    try:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=task_remimder_invalid_time_format + '\n' + 
                task_reminder_time,
            reply_markup=None
        )
        await message.delete()
    except Exception as error:
        logger.error(f"handle_reminder_invalid_time_input: {error}")