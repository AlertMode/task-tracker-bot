from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from modules.list.task_list_callback import (
    TaskStatus,
    TaskStatusCallbackData
)
from modules.alter.task_alteration_callback import (
    TaskAlterationAction,
    TaskAlterationCallbackData,
    TaskEditAction,
    TaskEditCallbackData
)
from utils.dictionary import *
from database.database import TaskStatus


return_to_edit_menu_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=MenuNames.EDIT_MENU)
    ]
], resize_keyboard=True, one_time_keyboard=True)


def task_ongoing_kb(task_id) -> InlineKeyboardMarkup:
    button_task_done_kb = InlineKeyboardButton(
        text=btn_task_done,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.DONE,
            id=task_id,
            status=TaskStatus.ONGOING
        ).pack()
    )
    button_task_edit_kb = InlineKeyboardButton(
        text=btn_task_edit,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.EDIT,
            id=task_id,
            status=TaskStatus.ONGOING
        ).pack()
    )
    button_task_delete_kb = InlineKeyboardButton(
        text=btn_task_delete,
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
    buttons_row_one = [button_task_done_kb, button_task_delete_kb]
    buttons_row_two = [button_task_edit_kb, button_ongoing_tasks]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            buttons_row_one,
            buttons_row_two
        ]
    )
    return markup


def task_completed_kb(task_id) -> InlineKeyboardMarkup:
    button_task_undone_kb = InlineKeyboardButton(
        text=btn_task_undone,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.UNDONE,
            id=task_id,
            status=TaskStatus.COMPLETED
        ).pack()
    )
    button_task_delete_kb = InlineKeyboardButton(
        text=btn_task_delete,
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


def task_edit_kb(task_id) -> InlineKeyboardMarkup:
    button_change_description = InlineKeyboardButton(
        text=btn_task_edit_description,
        callback_data=TaskEditCallbackData(
            action=TaskEditAction.CHANGE_DESCRIPTION,
            id=task_id,
            status=TaskStatus.ONGOING
        ).pack()
    )
    button_change_date = InlineKeyboardButton(
        text=btn_task_edit_date,
        callback_data=TaskEditCallbackData(
            action=TaskEditAction.CHANGE_DATE,
            id=task_id,
            status=TaskStatus.ONGOING
        ).pack()
    )
    button_change_time_zone = InlineKeyboardButton(
        text=btn_task_edit_timezone,
        callback_data=TaskEditCallbackData(
            action=TaskEditAction.CHANGE_TIME_ZONE,
            id=task_id,
            status=TaskStatus.ONGOING
        ).pack()
    )
    button_change_time = InlineKeyboardButton(
        text=btn_task_edit_time,
        callback_data=TaskEditCallbackData(
            action=TaskEditAction.CHANGE_TIME,
            id=task_id,
            status=TaskStatus.ONGOING
        ).pack()
    )
    button_return = InlineKeyboardButton(
        text=btn_common_return,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.SELECT,
            id=task_id,
            status=TaskStatus.ONGOING
        ).pack()
    )
    buttons_row_one = [
        button_change_description,
        button_change_date
    ]
    buttons_row_two = [
        button_change_time_zone,
        button_change_time
    ]
    buttons_row_three = [
        button_return
    ]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            buttons_row_one,
            buttons_row_two,
            buttons_row_three
        ]
    )
    return markup