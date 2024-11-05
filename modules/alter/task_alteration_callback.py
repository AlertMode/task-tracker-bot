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
    SELECT = auto()


class TaskEditAction(IntEnum):
    CHANGE_DESCRIPTION = auto()
    CHANGE_DATE = auto()
    CHANGE_TIME_ZONE = auto()
    CHANGE_TIME = auto()


class TaskAlterationCallbackData(CallbackData, prefix='task_alteration'):
    action: TaskAlterationAction
    id: int
    status: TaskStatus


class TaskEditCallbackData(CallbackData, prefix='task_edit'):
    action: TaskEditAction
    id: int
    status: TaskStatus