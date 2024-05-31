from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.common_commands_callback import (
    MenuCommands,
    MenuCommandsCallback
)
from callbacks.task_alteration_callback import (
    TaskStatus,
    TaskAlterationAction,
    TaskStatusCallbackData,
    TaskAlterationCallbackData
)
from utils.dictionary import *
from database.database import TaskStatus


ONGOING_TASKS = '▶️ Ongoing'
COMPLETED_TASKS = '⏹️ Completed'


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
    button_start = InlineKeyboardButton(
        text=MenuNames.MAIN_MENU,
        callback_data=MenuCommandsCallback(
            option=MenuCommands.START
        ).pack()
    )
    row_one = [button_ongoing_tasks, button_completed_tasks]
    row_two = [button_start]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[row_one, row_two]
    )
    return markup


def task_list_kb(tasks) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for task in tasks:
        builder.button(
            text=task.description,
            callback_data=TaskAlterationCallbackData(
                action=TaskAlterationAction.SKIP,
                id=task.id
            )
        )
    builder.button(
        text=button_tasks_back,
        callback_data=MenuCommandsCallback(
            option=MenuCommands.GET_TASKS
        )
    )
    builder.adjust(1)
    return builder.as_markup()


def task_ongoing_kb(task_id) -> InlineKeyboardMarkup:
    button_task_done_kb = InlineKeyboardButton(
        text=button_task_done,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.DONE,
            id=task_id
        ).pack()
    )
    button_task_edit_kb = InlineKeyboardButton(
        text=button_task_edit,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.EDIT,
            id=task_id
        ).pack()
    )
    button_task_delete_kb = InlineKeyboardButton(
        text=button_task_delete,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.DELETE,
            id=task_id
        ).pack()
    )
    button_ongoing_tasks = InlineKeyboardButton(
        text=button_tasks_back,
        callback_data=TaskStatusCallbackData(
            type=TaskStatus.ONGOING
        ).pack()
    )
    buttons_row_one = [button_task_done_kb, button_task_edit_kb]
    buttons_row_two = [button_task_delete_kb]
    button_row_three = [button_ongoing_tasks]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            buttons_row_one,
            buttons_row_two,
            button_row_three
        ]
    )
    return markup


def task_completed_kb(task_id) -> InlineKeyboardMarkup:
    button_task_undone_kb = InlineKeyboardButton(
        text=button_task_undone,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.UNDONE,
            id=task_id
        ).pack()
    )
    button_task_delete_kb = InlineKeyboardButton(
        text=button_task_delete,
        callback_data=TaskAlterationCallbackData(
            action=TaskAlterationAction.DELETE,
            id=task_id
        ).pack()
    )
    button_completed_tasks = InlineKeyboardButton(
        text=button_tasks_back,
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