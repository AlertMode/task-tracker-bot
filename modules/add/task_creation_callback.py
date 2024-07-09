from enum import (
    IntEnum,
    StrEnum,
    auto
)

from aiogram.filters.callback_data import CallbackData

class ReminderType(IntEnum):
    SINGLE = auto()
    RECURRING = auto()


class ReminderTypeCallbackData(CallbackData, prefix='reminder_type'):
    type: ReminderType
