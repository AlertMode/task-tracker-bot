from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from core.dictionary import *


def start_kb() -> ReplyKeyboardMarkup:
    button_new_task = KeyboardButton(text=MainMenuReplyKeyboard.NEW_TASK)
    button_get_tasks = KeyboardButton(text=MainMenuReplyKeyboard.GET_TASKS)
    buttons_first_row = [button_new_task, button_get_tasks]
    markup = ReplyKeyboardMarkup(
        keyboard=[buttons_first_row],
        resize_keyboard=True
    )
    return markup
