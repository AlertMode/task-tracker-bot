from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from database.database import DataBase
from database.models import Tasks
from core.dictionary import *

def choose_task_type_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=f'Ongoing', callback_data=f'ongoing_tasks')
    keyboard.button(text=f'Completed', callback_data=f'completed_tasks')
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


def actions_kb(task_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=f'{button_task_done}', callback_data=f'task_done_{task_id}')
    keyboard.button(text=f'{button_task_edit}', callback_data=f'task_edit_{task_id}')
    keyboard.button(text=f'{button_task_delete}', callback_data=f'task_delete_{task_id}')
    keyboard.adjust(2)
    return keyboard.as_markup()