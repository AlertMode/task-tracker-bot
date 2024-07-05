from venv import logger

from aiogram.types import (
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup
)

from callbacks.common_callback import *
from callbacks.task_creation_callback import *
from utils.dictionary import *


return_to_main_menu_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=MenuNames.MAIN_MENU)
    ]
], resize_keyboard=True, one_time_keyboard=True)


def reminder_type_selection_kb() -> InlineKeyboardMarkup:
    """
    Generates the keyboard for selecting the reminder options for a task.
    
    Returns:
        InlineKeyboardMarkup: The keyboard for selecting the reminder options for a task.
    """
    try:
        button_single = InlineKeyboardButton(
            text=button_task_reminder_single,
            callback_data=ReminderTypeCallbackData(
                type=ReminderType.SINGLE,
            ).pack()
        )
        button_recurring = InlineKeyboardButton(
            text=button_task_reminder_recurring,
            callback_data=ReminderTypeCallbackData(
                type=ReminderType.RECURRING
            ).pack()
        )
        button_skip = InlineKeyboardButton(
            text=button_common_skip,
            callback_data=CommonActionCallbackData(
                type=ReminderType.RECURRING,
                action=CommonAction.SKIP
            ).pack()
        )
        row_one = [button_single, button_recurring]
        row_two = [button_skip]
        markup = InlineKeyboardMarkup(
            inline_keyboard=[row_one, row_two]
        )
        return markup
    except Exception as error:
        logger.error(f"reminder_type_selection_kb: {error}")


def create_toggle_day_button(day: DayOfWeek, selected_days: set) -> InlineKeyboardButton:
    """
    Generates a button for toggling the day selection.

    Args:
        day (DayOfWeek): The day of the week.
        selected_days (set): The set of selected days.
    
    Returns:
        InlineKeyboardButton: The button for toggling the day selection.
    """
    try:
        return InlineKeyboardButton(
            text=(button_task_reminder_checked 
                if day in selected_days 
                else button_task_reminder_unchecked
                ) % day.value,
            callback_data=ReminderDayCallbackData(
                day=day.value,
                # Mark the day as selected if it is not in the set of selected days.
                selected = day.value not in selected_days
            ).pack()
        )
    except Exception as error:
        logger.error(f"create_toggle_day_button: {error}")


def recurring_day_selection_kb(selected_days: set) -> InlineKeyboardMarkup:
    """
    Generates the keyboard for selecting the days for a recurring reminder.

    Args:
        selected_days (set): The set of selected days.

    Returns:
        InlineKeyboardMarkup: The keyboard for selecting the days for a recurring reminder.
    """
    try:
        days_buttons = [create_toggle_day_button(day, selected_days) for day in DayOfWeek]
        control_buttons = []
        control_buttons.append(
            InlineKeyboardButton(
                text=button_common_confirm,
                callback_data=CommonActionCallbackData(
                    action=CommonAction.CONFIRM
                ).pack()
            )
        )
        control_buttons.append(
            InlineKeyboardButton(
                text=button_common_skip,
                callback_data=CommonActionCallbackData(
                    action=CommonAction.SKIP
                ).pack()
            )
        )
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                days_buttons[:2],
                days_buttons[2:5],
                days_buttons[5:],
                control_buttons
            ],
            resize_keyboard=True
        )
        return markup
    except Exception as error:
        logger.error(f"recurring_day_selection_kb: {error}")