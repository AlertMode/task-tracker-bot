from enum import (
    auto,
    IntEnum
)

from aiogram.filters.callback_data import CallbackData

from modules.list.task_list_callback import TaskStatus


class TaskAlterationAction(IntEnum):
    DONE = auto()
    UNDONE = auto()
    EDIT = auto()
    DELETE = auto()
    SKIP = auto()


class TaskAlterationCallbackData(CallbackData, prefix='task_alteration'):
    action: TaskAlterationAction
    id: int
    status: TaskStatus