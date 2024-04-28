from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from core.dictionary import *

def start_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text=start_list_text)
    kb.button(text=start_tasks_text)
    kb.button(text=start_add_list_text)
    kb.button(text=start_add_task_text)
    return kb.as_markup(resize_keyboard=True)
