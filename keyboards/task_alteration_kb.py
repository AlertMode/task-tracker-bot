from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.dictionary import *
from database.database import TaskStatus


ONGOING_TASKS = '▶️ Ongoing'
COMPLETED_TASKS = '⏹️ Completed'


class TaskAlterationAction(IntEnum):
    done = auto()
    undone = auto()
    edit = auto()
    delete = auto()


class TaskStatusCallbackData(CallbackData, prefix='task_type'):
    type: TaskStatus


class TaskAlterationCallbackData(CallbackData, prefix='task_alteration'):
    action: TaskAlterationAction
    id: int


def task_type_kb() -> InlineKeyboardMarkup:
    button_ongoing_tasks = InlineKeyboardButton(
        text=ONGOING_TASKS,
        callback_data=TaskStatusCallbackData(
            type=TaskStatus.ONGOING
        ).pack()
    )
    button_completed_tasks = InlineKeyboardButton(
        text=COMPLETED_TASKS,
        callback_data=TaskStatusCallbackData(
            type=TaskStatus.COMPLETED
        ).pack()
    )
    row = [button_ongoing_tasks, button_completed_tasks]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[row]
    )
    return markup


def task_ongoing_kb(task_id) -> InlineKeyboardMarkup:
    button_task_done_kb = InlineKeyboardButton(
        text=button_task_done,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.done,
            id=task_id
        ).pack()
    )
    button_task_edit_kb = InlineKeyboardButton(
        text=button_task_edit,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.edit,
            id=task_id
        ).pack()
    )
    button_task_delete_kb = InlineKeyboardButton(
        text=button_task_delete,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.delete,
            id=task_id
        ).pack()
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


def task_completed_kb(task_id) -> InlineKeyboardMarkup:
    button_task_undone_kb = InlineKeyboardButton(
        text=button_task_undone,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.undone,
            id=task_id
        ).pack()
    )
    button_task_delete_kb = InlineKeyboardButton(
        text=button_task_delete,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.delete,
            id=task_id
        ).pack()
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