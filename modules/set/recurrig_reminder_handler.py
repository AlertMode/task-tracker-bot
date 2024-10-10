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
from modules.set.recurring_reminder_kb import *
from utils.dictionary import *


router = Router(name=__name__)


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
        await callback.message.delete()
        state_data = await state.get_data()
        selected_days = state_data.get('selected_days', set())

        #Using only one callback for both reminder type and day selection.
        callback_data = callback.data

        if 'reminder_type' in callback_data:
            await callback.message.delete()
            await callback.message.answer(
                text=task_reminder_message,
                reply_markup=recurring_day_selection_kb(set())
            )
            await state.update_data(reminder_type = ReminderType.RECURRING)

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
            await state.set_state(CreateState.time)

    except Exception as error:
        logger.error(f"handle_day_selection: {error}")


@router.message(
CreateState.time,
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
    #TODO: Still find the the way to delete the messagesm, but withoug using states
    try:
        await message.delete()
        await state.update_data(reminder_time=time)
        await state.set_state(CreateState.reminder_interval_type)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=task_reminder_interval_selection,
            reply_markup=reminder_interval_selection_kb()
        )
    except Exception as error:
        logger.error(f"handle_reminder_time_input: {error}")


@router.message(
    CreateState.time
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
        await callback.message.delete()
        await state.set_state(CreateState.reminder_interval_number)
        await callback.message.answer(
            text=msg_reminder_interval_number,
            reply_markup=None
        )
        await state.update_data(interval_type=callback_data.interval.value)
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

        date = calculate_next_reminder_date(
            type=interval_type,
            initial_datetime=reminder_time,
            interval=interval_number
        )

        await state.update_data(next_reminder_date=date)
        data = await state.get_data()
        next_reminder_date = data.get('next_reminder_date')

        await state.set_state(CreateState.final_confirmation)
        await message.answer(
            #TODO: Extend the message's variational part with days' selection or a single date
            text=msg_task_recurring_reminder_final_confirmation % (
                description_task,
                reminder_time,
                interval_number,
                interval_type,
                next_reminder_date
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