from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from modules.add.task_creation_callback import *
from modules.add.task_creation_kb import *
from modules.add.task_creation_state import CreateState
from modules.common.auxilary_handler import *
from modules.set.reminder_recurring_kb import *
from modules.set.time_handler import router as time_router
from utils.dictionary import *


router = Router(name=__name__)
router.include_router(router=time_router)


@router.callback_query(
    CreateState.reminder_type,
    ReminderTypeCallbackData.filter(
        F.type == ReminderType.RECURRING
    )
)
@router.callback_query(
    ReminderDayCallbackData.filter(
        F.selected != None
    )
)
@router.callback_query(
    CreateState.reminder_type,
    CommonActionCallbackData.filter(
        F.action == CommonAction.CONFIRM
    )
)
async def handle_day_selection(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """
    Handles the selection of the days for a recurring reminder.

    Args:
        callback (CallbackQuery): The callback query object.
        state (FSMContext): The FSM context object.

    Returns:
        None
    """
    try:
        await callback.answer()
        state_data = await state.get_data()
        selected_days = state_data.get('selected_days', set())

        #Using only one callback for both reminder type and day selection.
        callback_data = callback.data

        if 'reminder_type' in callback_data:
            await callback.message.answer(
                text=task_reminder_message,
                reply_markup=recurring_day_selection_kb(set())
            )
            await callback.message.delete()

        elif 'reminder_day' in callback_data:
            _, day, _ = callback_data.split(':')

            if day in selected_days:
                selected_days.remove(day)
            else:
                selected_days.add(day)
            await state.update_data(selected_days=selected_days)
            
            # Update the keyboard with the new selection.
            await callback.message.edit_reply_markup(
                reply_markup=recurring_day_selection_kb(selected_days)
            )

        elif ('common_action' in callback_data) and len(selected_days) != 0:
            await callback.message.answer(
                text=task_reminder_time,
                reply_markup=None
            )
            await state.set_state(CreateState.reminder_time)
            await callback.message.delete()

    except Exception as error:
        logger.error(f"handle_day_selection: {error}")


@router.callback_query(
        CreateState.reminder_interval,
        
                       )
async def handle_recurring_interval_selection(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """
    Handles the selection of the interval for a recurring reminder.

    Args:
        callback (CallbackQuery): The callback query object.
        state (FSMContext): The FSM context object.

    Returns:
        None
    """
    #TODO: Complete the logic.
    try:
        await callback.answer()
        await delete_all_messages(
            state=state,
            bot=callback.bot,
            chat_id=callback.from_user.id
        )
        await callback.message.answer(
            text='DONE!',
            reply_markup=None
        )
        await state.set_state(CreateState.reminder_time)
        await callback.message.delete()
    except Exception as error:
        logger.error(f"handle_recurring_interval_selection: {error}")



