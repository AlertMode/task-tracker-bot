from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from callbacks.common_commands_callback import (
    MenuCommands,
    MenuCommandsCallback
)
from callbacks.task_list_callback import (
    TaskStatus,
    TaskStatusCallbackData
)
from callbacks.task_alteration_callback import (
    TaskAlterationAction,
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


def task_list_kb(tasks, current_page=0, task_status=TaskStatus.ONGOING) -> InlineKeyboardMarkup:
    tasks_per_page = 10
    start_index = current_page * tasks_per_page
    end_index = start_index + tasks_per_page
    paginated_tasks = tasks[start_index:end_index]

    buttons = []
    for task in paginated_tasks:
        buttons.append([
            InlineKeyboardButton(
                text=task.description,
                callback_data=TaskAlterationCallbackData(
                    action=TaskAlterationAction.SKIP,
                    id=task.id
                ).pack()
            )
        ])

    total_pages = (len(tasks) - 1) // tasks_per_page + 1
    navigation_buttons_row_one = []
    navigation_buttons_row_two = []

    if current_page > 0:
        navigation_buttons_row_one.append(
            InlineKeyboardButton(
                text=button_common_backwards,
                callback_data=TaskStatusCallbackData(
                    type=task_status,
                    page=current_page - 1
                ).pack()
            )
        )
    navigation_buttons_row_one.append(
        InlineKeyboardButton(
            text=f"{current_page + 1}/{total_pages}",
            callback_data="page_info"
        )
    )
    if end_index < len(tasks):
        navigation_buttons_row_one.append(
            InlineKeyboardButton(
                text=button_common_forward,
                callback_data=TaskStatusCallbackData(
                    type=task_status,
                    page=current_page + 1
                ).pack()
            )
        )
    navigation_buttons_row_two.append(
        InlineKeyboardButton(
            text=button_common_return,
            callback_data=MenuCommandsCallback(
                option=MenuCommands.GET_TASKS
            ).pack()
        )
    )
    
    if navigation_buttons_row_one:
        buttons.append(navigation_buttons_row_one)
        buttons.append(navigation_buttons_row_two)

    return InlineKeyboardMarkup(inline_keyboard=buttons)
