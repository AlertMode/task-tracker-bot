from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from modules.common.actions_callback import *
from modules.set.reminder_recurring_callback import *
from utils.dictionary import *
from utils.logging_config import logger


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
                text=btn_common_confirm,
                callback_data=CommonActionCallbackData(
                    action=CommonAction.CONFIRM
                ).pack()
            )
        )
        control_buttons.append(
            InlineKeyboardButton(
                text=btn_common_skip,
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



def reminder_interval_selection_kb() -> InlineKeyboardMarkup:
    """
    Generates the keyboard for selecting the interval of the reminder.

    Returns:
        InlineKeyboardMarkup: The keyboard for selecting the interval of the reminder.
    """
    try:
        button_daily = InlineKeyboardButton(
            text=button_task_reminder_daily,
            callback_data=ReminderIntervalCallbackData(
                interval=ReminderInterval.BY_DAYS
            ).pack()
        )
        button_weekly = InlineKeyboardButton(
            text=button_task_reminder_weekly,
            callback_data=ReminderIntervalCallbackData(
                interval=ReminderInterval.BY_WEEKS
            ).pack()
        )
        button_monthly = InlineKeyboardButton(
            text=button_task_reminder_monthly,
            callback_data=ReminderIntervalCallbackData(
                interval=ReminderInterval.BY_MONTHS
            ).pack()
        )
        button_yearly = InlineKeyboardButton(
            text=button_task_reminder_yearly,
            callback_data=ReminderIntervalCallbackData(
                interval=ReminderInterval.BY_YEARS
            ).pack()
        )
        button_skip = InlineKeyboardButton(
            text=btn_common_skip,
            callback_data=CommonActionCallbackData(
                action=CommonAction.SKIP
            ).pack()
        )
        row_one = [button_daily, button_weekly]
        row_two = [button_monthly, button_yearly]
        row_three = [button_skip]
        markup = InlineKeyboardMarkup(
            inline_keyboard=[row_one, row_two, row_three]
        )
        return markup
    except Exception as error:
        logger.error(f"reminder_interval_selection: {error}")


#TODO: Write a keyboard for selecting
# the interval's value (e.g. every 2 days, every 3 weeks, etc.)