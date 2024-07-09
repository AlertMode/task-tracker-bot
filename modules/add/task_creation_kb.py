from aiogram.types import (
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup
)

from modules.common.actions_callback import *
from modules.add.task_creation_callback import *
from utils.dictionary import *
from utils.logging_config import logger


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