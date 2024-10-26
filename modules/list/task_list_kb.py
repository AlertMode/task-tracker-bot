from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from modules.common.commands_callback import (
    MenuCommands,
    MenuCommandsCallback
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


def task_type_kb() -> InlineKeyboardMarkup:
    """
    Generates the keyboard for selecting the type of tasks to display.
    
    Returns:
        InlineKeyboardMarkup: The keyboard for selecting the type of tasks to display.
    """
    button_ongoing_tasks = InlineKeyboardButton(
        text=ongoing_tasks,
        callback_data=TaskStatusCallbackData(
            type=TaskStatus.ONGOING
        ).pack()
    )
    button_completed_tasks = InlineKeyboardButton(
        text=completed_tasks,
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


def task_list_kb(tasks, current_page=0, task_status=TaskStatus.ONGOING, from_the_end=False) -> InlineKeyboardMarkup:
    """
    Generates the keyboard for the task list.

    Args:
        tasks (List[Task]): The list of tasks to display.
        current_page (int): The current page of the task list.
        task_status (TaskStatus): The status of the tasks to display.
        from_the_end (bool): Whether to display the last page of the task list.
    
    Returns:
        InlineKeyboardMarkup: The keyboard for the task list.
    """
    tasks_per_page = 10
    total_pages = (len(tasks) - 1) // tasks_per_page + 1

    if from_the_end:
        current_page = total_pages - 1

    start_index = current_page * tasks_per_page
    end_index = start_index + tasks_per_page
    paginated_tasks = tasks[start_index:end_index]

    buttons = []
    for task in paginated_tasks:
        buttons.append([
            InlineKeyboardButton(
                text=task.description,
                callback_data=TaskAlterationCallbackData(
                    action=TaskAlterationAction.SELECT,
                    id=task.id,
                    status=task_status
                ).pack()
            )
        ])

    navigation_buttons_row_one = []
    navigation_buttons_row_two = []

    if current_page > 0:
        navigation_buttons_row_one.append(
            InlineKeyboardButton(
                text=btn_common_backwards,
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
                text=btn_common_forward,
                callback_data=TaskStatusCallbackData(
                    type=task_status,
                    page=current_page + 1
                ).pack()
            )
        )
    navigation_buttons_row_two.append(
        InlineKeyboardButton(
            text=btn_common_return,
            callback_data=MenuCommandsCallback(
                option=MenuCommands.GET_TASKS
            ).pack()
        )
    )
    
    if navigation_buttons_row_one:
        buttons.append(navigation_buttons_row_one)
        buttons.append(navigation_buttons_row_two)

    return InlineKeyboardMarkup(inline_keyboard=buttons)
