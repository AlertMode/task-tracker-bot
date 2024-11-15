from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.database import DataBase
from modules.add.task_creation_state import CreateTaskState
from modules.alter.task_alteration_kb import task_edit_kb
from modules.alter.task_alteration_state import AlterTaskState
from modules.common.auxilary_handler import *
from modules.set.time_picker_kb import create_time_picker_keyboard
from modules.set.time_zone_selector_callback import *
from utils.dictionary import *
from utils.logging_config import logger


db = DataBase()
router = Router(name=__name__)


@router.callback_query(
        TimeZoneSelectorCallbackData.filter(),
        CreateTaskState.time_zone
)
@router.callback_query(
        TimeZoneSelectorCallbackData.filter(),
        AlterTaskState.edit_time_zone
)
async def handle_time_zone_selector(
    callback: CallbackQuery,
    callback_data: TimeZoneSelectorCallbackData,
    state: FSMContext
) -> None:
    """
    Handles the time zone selector callback query.

    Args:
        callback (CallbackQuery): The callback query instance.
        callback_data (TimeZoneSelectorCallbackData): The time zone selector callback data.
        state (FSMContext): The FSM context.

    Returns:
        None
    """
    try:
        selected_time_zone = callback_data.time_zone
        current_state = await state.get_state()

        if current_state == CreateTaskState.time_zone.state:
            await state.update_data(time_zone=selected_time_zone)
            await state.set_state(CreateTaskState.time_picker)
            await callback.message.answer(
                text=msg_task_reminder_time_picker,
            reply_markup=create_time_picker_keyboard()
        )
            
        elif current_state == AlterTaskState.edit_time_zone.state:
            data = await state.get_data()
            task_id = data.get("task_id")
            await db.update_task_reminder_utc(task_id, selected_time_zone)
            await db.set_task_not_reminded(task_id)
            await state.clear()
            await callback.message.answer(
                text=(f'{msg_task_timezone_change_completed}\n\n{selected_time_zone}'),
                reply_markup=task_edit_kb(task_id)
            )

        await callback.answer()
        await callback.message.delete()
    except Exception as error:
        logger.error(f"handle_time_zone_selector: {error}")
        await callback.answer("An error occurred while selecting the time zone.")