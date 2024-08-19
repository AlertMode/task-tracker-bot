from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from modules.list.task_list_callback import (
    TaskStatus,
    TaskStatusCallbackData
)
from modules.alter.task_alteration_callback import (
    TaskAlterationAction,
    TaskAlterationCallbackData
)
from utils.dictionary import *
from database.database import TaskStatus


def task_ongoing_kb(task_id) -> InlineKeyboardMarkup:
    button_task_done_kb = InlineKeyboardButton(
        text=button_task_done,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.DONE,
            id=task_id,
            status=TaskStatus.ONGOING
        ).pack()
    )
    #TODO: Implement the edit task functionality. Somday...

    # button_task_edit_kb = InlineKeyboardButton(
    #     text=button_task_edit,
    #     callback_data=TaskAlterationCallbackData(
    #         action=TaskAlterationAction.EDIT,
    #         id=task_id,
    #         status=TaskStatus.ONGOING
    #     ).pack()
    # )
    button_task_delete_kb = InlineKeyboardButton(
        text=button_task_delete,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.DELETE,
            id=task_id,
            status=TaskStatus.ONGOING
        ).pack()
    )
    button_ongoing_tasks = InlineKeyboardButton(
        text=btn_common_return,
        callback_data=TaskStatusCallbackData(
            type=TaskStatus.ONGOING
        ).pack()
    )
    buttons_row_one = [button_task_done_kb, button_task_delete_kb ]
    buttons_row_two = [button_ongoing_tasks]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            buttons_row_one,
            buttons_row_two
        ]
    )
    return markup


def task_completed_kb(task_id) -> InlineKeyboardMarkup:
    button_task_undone_kb = InlineKeyboardButton(
        text=button_task_undone,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.UNDONE,
            id=task_id,
            status=TaskStatus.COMPLETED
        ).pack()
    )
    button_task_delete_kb = InlineKeyboardButton(
        text=button_task_delete,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.DELETE,
            id=task_id,
            status=TaskStatus.COMPLETED
        ).pack()
    )
    button_completed_tasks = InlineKeyboardButton(
        text=btn_common_return,
        callback_data=TaskStatusCallbackData(
            type=TaskStatus.COMPLETED
        ).pack()
    )
    buttons_row_one = [
        button_task_undone_kb,
        button_task_delete_kb
    ]
    buttons_row_two = [
        button_completed_tasks
    ]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            buttons_row_one,
            buttons_row_two
        ]
    )
    return markup