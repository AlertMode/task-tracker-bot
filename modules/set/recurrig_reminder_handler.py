from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from modules.add.task_creation_callback import *
from modules.common.auxilary_handler import *
from modules.add.task_creation_kb import *
from modules.add.task_creation_state import CreateState
from utils.dictionary import *


router = Router(name=__name__)


@router.callback_query(
    CreateState.reminder_type,
    ReminderTypeCallbackData.filter(
        F.type == ReminderType.RECURRING
    )
)
async def handle_recurring_reminder_listener(
    callback: CallbackQuery
) -> None:
    try:
        await callback.answer()
        await callback.message.answer(
            text=task_reminder_message,
            reply_markup=recurring_day_selection_kb(set())
        )
        await callback.message.delete()
    except Exception as error:
        logger.error(f"handle_recurring_reminder_selection: {error}")


@router.callback_query(
    ReminderDayCallbackData.filter(
        F.selected != None
    )
)
async def handle_recurring_reminder_selection_callback(
    callback: CallbackQuery,
    callback_data: ReminderDayCallbackData,
    state: FSMContext
) -> None:
    try:
        data = await state.get_data()
        selected_days = data.get('selected_days', set())

        # Toggle the day selection in the set of selected days for the keybaord.
        if callback_data.day in selected_days:
            selected_days.remove(callback_data.day)
        else:
            selected_days.add(callback_data.day)

        await state.update_data(selected_days=selected_days)
        
        # Update the keyboard with the new selection.
        new_markup = recurring_day_selection_kb(selected_days)
        await callback.message.edit_reply_markup(
            reply_markup=new_markup
        )
        await store_message_id(
            state=state,
            message_id=callback.message.message_id)
        await callback.answer()
    except Exception as error:
        logger.error(f"handle_recurring_reminder_selection_callback: {error}")
