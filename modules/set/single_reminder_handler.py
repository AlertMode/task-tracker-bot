from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram3_calendar import SimpleCalendar
from aiogram3_calendar.calendar_types import SimpleCalendarCallback

from modules.add.task_creation_callback import *
from modules.add.task_creation_kb import *
from modules.add.task_creation_state import CreateState
from modules.common.auxilary_handler import *
from modules.set.time_zone_selector_kb import create_time_zone_keyboard
from utils.dictionary import *
from utils.logging_config import logger

from modules.set.time_zone_selector_handler import router as time_zone_selector_router

router = Router(name=__name__)
router.include_router(time_zone_selector_router)


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
            reply_markup = await SimpleCalendar().start_calendar()
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
        await state.update_data(date = date)
        await state.set_state(CreateState.time_zone)
        await callback.message.answer(
            text=task_reminder_timezone,
            reply_markup=create_time_zone_keyboard()
)