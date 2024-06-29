from enum import (
    IntEnum,
    StrEnum,
    auto
)

from aiogram.filters.callback_data import CallbackData

from callbacks.common_callback import *

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


class ReminderTypeCallbackData(CallbackData, prefix='reminder_type'):
    type: ReminderType


class ReminderDayCallbackData(CallbackData, prefix='reminder_day'):
    day: DayOfWeek = None
    selected: bool = False
