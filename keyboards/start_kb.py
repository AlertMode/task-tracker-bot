from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.dictionary import (
    MenuCommands,
    MenuNames
)


class MenuCommandsCallback(CallbackData, prefix='main_menu'):
    action: MenuCommands


def start_kb() -> InlineKeyboardMarkup:
    button_new_task = InlineKeyboardButton(
        text=MenuNames.NEW_TASK,
        callback_data=MenuCommandsCallback(
            action=MenuCommands.CREATE_TASK
        ).pack()
    )
    button_get_tasks = InlineKeyboardButton(
        text=MenuNames.GET_TASKS,
        callback_data=MenuCommandsCallback(
            action=MenuCommands.GET_TASKS
        ).pack()
    )
    row = [button_new_task, button_get_tasks]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[row]
    )
    return markup
