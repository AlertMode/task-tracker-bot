from enum import (
    IntEnum,
    StrEnum,
    auto
)

from aiogram.filters.callback_data import CallbackData


class ReminderType(IntEnum):
    SINGLE = auto()
    RECURRING = auto()

class DayOfWeek(StrEnum):
    MONDAY = 'MONDAY'
    TUESDAY = 'TUESDAY'
    WEDNESDAY = 'WEDNESDAY'
    THURSDAY = 'THURSDAY'
    FRIDAY = 'FRIDAY'
    SATURDAY = 'SATURDAY'
    SUNDAY = 'SUNDAY'


class ReminderAction(IntEnum):
    TOGGLE = auto()
    CONFIRM = auto()
    BACK = auto()
    SKIP = auto()


class ReminderCallbackData(CallbackData, prefix='reminder_info'):
    type: ReminderType
    action: ReminderAction
    day: DayOfWeek = None
    selected: bool = False
