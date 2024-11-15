from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from aiogram3_calendar import SimpleCalendar
from aiogram3_calendar.calendar_types import SimpleCalendarCallback

from database.database import DataBase
from modules.add.task_creation_state import CreateTaskState
from modules.add.task_creation_kb import *
from modules.alter.task_alteration_kb import task_edit_kb
from modules.alter.task_alteration_state import AlterTaskState
from modules.set.time_zone_selector_kb import create_time_zone_keyboard
from utils.dictionary import *

db = DataBase()
router = Router(name=__name__)


@router.callback_query(
    CreateTaskState.date,
    SimpleCalendarCallback.filter()
)
@router.callback_query(
    AlterTaskState.edit_date,
    SimpleCalendarCallback.filter()
)
async def handle_simple_calendar_date_selection(
    callback: CallbackQuery,
    callback_data: dict,
    state: FSMContext
) -> None:
    try:
        await callback.answer()
        selected, date = await SimpleCalendar().process_selection(callback, callback_data)
        if selected:
            current_state = await state.get_state()

            if current_state == CreateTaskState.date.state:
                await state.update_data(date = date)
                await state.set_state(CreateTaskState.time_zone)
                await callback.message.answer(
                    text=msg_task_reminder_timezone,
                    reply_markup=create_time_zone_keyboard()
                )
                

            elif current_state == AlterTaskState.edit_date.state:
                task_id = (await state.get_data()).get('task_id')
                task = await db.get_task_by_id(task_id)
                original_date = task.reminder_date
                replaced_date = original_date.replace(
                    year=date.year,
                    month=date.month,
                    day=date.day
                )
                await db.update_task_reminder_date(
                    task_id=task_id,
                    reminder_date=replaced_date
                )
                await db.set_task_not_reminded(task_id=task_id)
                await state.clear()
                await callback.message.answer(
                    text=(f'{msg_task_date_change_completed}\n\n{replaced_date.strftime('%Y-%m-%d')}'),
                    reply_markup=task_edit_kb(task_id)
                )
                
            await callback.message.delete()

    except Exception as error:
        logger.error(f"handle_simple_calendar_date_selection: {error}")
        await state.clear()