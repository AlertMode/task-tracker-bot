from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton

from core.dictionary import *


ONGOING_TASKS = '▶️ Ongoing'
COMPLETED_TASKS = '⏹️ Completed'


def choose_task_type_kb() -> ReplyKeyboardMarkup:
    button_ongoing_tasks = KeyboardButton(text=ONGOING_TASKS)
    button_compeleted_tasks = KeyboardButton(text=COMPLETED_TASKS)
    buttons_first_row = [button_ongoing_tasks]
    buttons_second_row = [button_compeleted_tasks]
    markup = ReplyKeyboardMarkup(
        keyboard=[buttons_first_row, buttons_second_row],
        resize_keyboard=True
    )
    return markup


def actions_kb(task_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=f'{button_task_done}', callback_data=f'task_done_{task_id}')
    keyboard.button(text=f'{button_task_edit}', callback_data=f'task_edit_{task_id}')
    keyboard.button(text=f'{button_task_delete}', callback_data=f'task_delete_{task_id}')
    keyboard.adjust(2)
    return keyboard.as_markup()