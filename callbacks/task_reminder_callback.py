from enum import (
    IntEnum,
    StrEnum,
    auto
)

from aiogram.filters.callback_data import CallbackData


class DayOfWeek(StrEnum):
    MONDAY = 'MONDAY'
    TUESDAY = 'TUESDAY'
    WEDNESDAY = 'WEDNESDAY'
    THURSDAY = 'THURSDAY'
    FRIDAY = 'FRIDAY'
    SATURDAY = 'SATURDAY'
    SUNDAY = 'SUNDAY'


class ReminderAction(IntEnum):
    TOGGLE_DAY = auto()
    CONFIRM = auto()
    BACK = auto()
    IS_RECURRING = auto()


class DayOfWeekCallbackData(CallbackData, prefix='day_of_week'):
    action: ReminderAction
    day: DayOfWeek = None
    selected: bool = False
