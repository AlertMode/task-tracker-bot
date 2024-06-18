from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from callbacks.task_reminder_callback import *
from utils.dictionary import *


def set_days_kb(selected_days, is_recurring) -> InlineKeyboardMarkup:
    buttons = []
    if selected_days is None:
        selected_days = []

    for day in DayOfWeek:
        is_selected = day in selected_days
        button_text = (button_task_reminder_checked % day.value 
                       if is_selected 
                       else button_task_reminder_unchecked % day.value)

        toggle_day_button = InlineKeyboardButton(
            text=button_text,
            callback_data=DayOfWeekCallbackData(
                action=ReminderAction.TOGGLE_DAY,
                day=day,
                selected=not is_selected
            ).pack()
        )
        buttons.append(toggle_day_button)

    
    if selected_days:
        confirm_button = InlineKeyboardButton(
            text=button_task_reminder_confirm,
            callback_data=DayOfWeekCallbackData(
                action=ReminderAction.CONFIRM
            ).pack()
        )
        buttons.append(confirm_button)
    else:
        skip_button = InlineKeyboardButton(
            text=button_task_reminder_skip,
            callback_data=DayOfWeekCallbackData(
                action=ReminderAction.SKIP
            ).pack()
        )
        buttons.append(skip_button)

    back_button = InlineKeyboardButton(
        text=button_common_backwards,
        callback_data=DayOfWeekCallbackData(
            action=ReminderAction.BACK
        ).pack()
    )
    is_recurring_button = InlineKeyboardButton(
        text=(button_common_number_one
                if not is_recurring
                else button_task_reminder_recurrence),
        callback_data=DayOfWeekCallbackData(
            action=ReminderAction.IS_RECURRING
        ).pack()
    )

    buttons.append(back_button)
    buttons.append(is_recurring_button)

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons[:3])
    keyboard.add(*buttons[3:6])
    keyboard.add(*buttons[6:9])
    keyboard.add(*buttons[9:])

    return keyboard
        
    