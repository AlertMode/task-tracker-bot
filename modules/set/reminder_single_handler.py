import logging
import asyncio
import sys
from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message
)
from aiogram3_calendar import SimpleCalendar
from aiogram3_calendar.calendar_types import (
    SimpleCalendarCallback,
    SimpleCalendarAction
)

from modules.add.task_creation_callback import *
from modules.add.task_creation_state import CreateState
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
    callback: CallbackQuery
) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        text="Please, select the date for the reminder.",
        reply_markup=await SimpleCalendar().start_calendar()
    )
    try:
        pass
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

        #TODO: Add the time selection below.
        await callback.message.answer(
            text=f"Selected date: {date}"
)