from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message
)
from aiogram3_calendar import SimpleCalendar
from aiogram3_calendar.calendar_types import SimpleCalendarCallback

from modules.add.task_creation_callback import *
from modules.add.task_creation_kb import *
from modules.add.task_creation_state import CreateState
from modules.common.auxilary_handler import *
from utils.dictionary import *
from utils.logging_config import logger


router = Router(name=__name__)


@router.callback_query(
    CreateState.reminder_type,
    ReminderTypeCallbackData.filter(
        F.type == ReminderType.SINGLE
    )
)
async def handle_single_reminder_listener(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    try:
        await callback.answer()
        await callback.message.delete()
        await state.update_data(reminder_type = ReminderType.SINGLE)
        await callback.message.answer(
            text="Please, select the date for the reminder.",
            reply_markup=await SimpleCalendar().start_calendar()
        )
    except Exception as error:
        logger.error(f"handle_calendar_date_selection: {error}")


@router.callback_query(
    SimpleCalendarCallback.filter()
)
async def handle_simple_calendar_date_selection(
    callback: CallbackQuery,
    callback_data: dict,
    state: FSMContext
) -> None:
    await callback.answer()
    selected, date = await SimpleCalendar().process_selection(callback, callback_data)
    if selected:
        await state.update_data(single_date = date)
        await state.set_state(CreateState.reminder_time)
        await callback.message.answer(
            text=task_reminder_time,
            reply_markup=None
)
        

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
    try:
        await message.delete()
        await state.update_data(reminder_time=time)

        data = await state.get_data()
        description_task = data.get('description_task')
        reminder_time = data.get('reminder_time')
        single_date = data.get('single_date')
        #TODO: Add time to the reminder date.

        await state.set_state(CreateState.final_confirmation)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=msg_task_single_reminder_final_confirmation % (
                description_task,
                single_date,
                reminder_time
            ),
            reply_markup=final_confirmation_kb()
        )
    except Exception as error:
        logger.error(f"handle_reminder_time_input: {error}")


@router.message(
    CreateState.reminder_time
)
async def handle_reminder_invalid_time_input(
    message: Message,
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
        await message.delete()
        await bot.send_message(
            chat_id=message.from_user.id,
            text=task_remimder_invalid_time_format + '\n' + 
            task_reminder_time,
            reply_markup=None
        )
    except Exception as error:
        logger.error(f"handle_reminder_invalid_time_input: {error}")