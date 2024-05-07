from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from core.dictionary import *


def start_kb():
    button_new_task = KeyboardButton(text=NEW_TASK)
    button_get_tasks = KeyboardButton(text=GET_TASKS)
    buttons_first_row = [button_new_task, button_get_tasks]
    markup = ReplyKeyboardMarkup(
        keyboard=[buttons_first_row],
        resize_keyboard=True
    )
    return markup
