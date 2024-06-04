from enum import (
    auto,
    IntEnum
)

from aiogram.filters.callback_data import CallbackData


class TaskAlterationAction(IntEnum):
    DONE = auto()
    UNDONE = auto()
    EDIT = auto()
    DELETE = auto()
    SKIP = auto()


class TaskAlterationCallbackData(CallbackData, prefix='task_alteration'):
    action: TaskAlterationAction
    id: int