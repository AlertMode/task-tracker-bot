from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message
)

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
        CreateState.reminder_interval_type,
        ReminderIntervalCallbackData.filter()
    )
async def handle_recurring_interval_selection(
    callback: CallbackQuery,
    callback_data: ReminderIntervalCallbackData,
    state: FSMContext
    ) -> None:
    """
    Handles the selection of the interval for a recurring reminder.

    Args:
        callback (CallbackQuery): The callback query object.
        callback_data (ReminderIntervalCallbackData): The callback data object.
        state (FSMContext): The FSM context object.

    Returns:
        None
    """
    try:
        #TODO: Figure out how to delete the previous messages.
        await callback.answer()
        await state.set_state(CreateState.reminder_interval_number)
        await callback.message.answer(
            text=msg_reminder_interval_number,
            reply_markup=None
        )
        await state.update_data(interval_type=callback_data.interval.value)
        await callback.message.delete()
    except Exception as error:
        logger.error(f"handle_recurring_interval_selection: {error}")

    
@router.message(
    CreateState.reminder_interval_number,
    F.text.cast(validate_interval_format).as_("interval")
)
async def handle_recurring_interval_number(
    message: Message,
    interval: int,
    state: FSMContext
) -> None:
    """
    Handles the selection of the interval number for a recurring reminder.

    Args:
        message (Message): The incoming message object.
        interval (int): The selected interval number.
        state (FSMContext): The FSM context object.

    Returns:
        None
    """
    try:
        await message.delete()
        await state.update_data(interval_number=interval)

        data = await state.get_data()
        description_task = data.get('description_task')
        reminder_time = data.get('reminder_time')
        interval_number = data.get('interval_number')
        interval_type = data.get('interval_type')

        print(f'interval_type: {interval_type}')

        # PLACEHOLDER: Calculate the quantity of days for the next reminder.
        interval_days = 42

        next_reminder = calculate_next_reminder_date(
            initial_datetime=reminder_time,
            days=interval_days
        )

        # await state.update_data(next_reminder=next_reminder)
        next_reminder = data.get('next_reminder')

        await state.update_data(next_reminder=next_reminder)
        await state.set_state(CreateState.final_confirmation)
        await message.answer(
            #TODO: Extend the message's variational part with days' selection or a single date
            text=msg_task_recurring_reminder_final_confirmation % (
                description_task,
                reminder_time,
                interval_number,
                interval_type,
                next_reminder
            ),
            reply_markup=final_confirmation_kb()
        )
    except Exception as error:
        logger.error(f"handle_recurring_interval_number: {error}")


@router.message(
    CreateState.reminder_interval_number
)
async def handle_invalid_interval_number(
    message: Message
) -> None:
    """
    Handles the invalid interval number for the recurring reminder.

    Args:
        message (Message): The incoming message object.

    Returns:
        None
    """
    try:
        await message.delete()
        #TODO: Add the original message's text to the warning
        await message.answer(
            text=msg_reminder_invalid_interval_number,
            reply_markup=None
        )
    except Exception as error:
        logger.error(f"handle_invalid_interval_number: {error}")