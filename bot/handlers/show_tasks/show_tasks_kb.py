from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

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


def ongoing_tasks_actions_kb(task_id) -> InlineKeyboardMarkup:
    button_task_done_kb = InlineKeyboardButton(
        text=button_task_done,
        callback_data=f'task_done_{task_id}'
    )
    button_task_edit_kb = InlineKeyboardButton(
        text=button_task_edit,
        callback_data=f'task_edit_{task_id}'
    )
    button_task_delete_kb = InlineKeyboardButton(
        text=button_task_delete,
        callback_data=f'task_delete_{task_id}'
    )
    buttons_first_row_kb = [button_task_done_kb, button_task_edit_kb]
    buttons_second_row_kb = [button_task_delete_kb]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            buttons_first_row_kb,
            buttons_second_row_kb
        ]
    )
    return markup


def completed_tasks_actions_kb(task_id) -> InlineKeyboardMarkup:
    button_task_undone_kb = InlineKeyboardButton(
        text=button_task_undone,
        callback_data=f'task_undone_{task_id}'
    )
    button_task_delete_kb = InlineKeyboardButton(
        text=button_task_delete,
        callback_data=f'task_delete_{task_id}'
    )
    buttons_row_kb = [
        button_task_undone_kb,
        button_task_delete_kb
    ]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            buttons_row_kb
        ]
    )
    return markup