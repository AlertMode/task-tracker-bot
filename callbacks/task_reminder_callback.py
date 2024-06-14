from enum import Enum

from aiogram.filters.callback_data import CallbackData


class DayOfWeek(Enum):
    MONDAY = 'MONDAY'
    TUESDAY = 'TUESDAY'
    WEDNESDAY = 'WEDNESDAY'
    THURSDAY = 'THURSDAY'
    FRIDAY = 'FRIDAY'
    SATURDAY = 'SATURDAY'
    SUNDAY = 'SUNDAY'


class ReminderAction(str, Enum):
    TOGGLE_DAY = "toggle_day"
    CONFIRM = "confirm"
    SKIP = "skip"
    BACK = "back"
    IS_RECURRING = "is_recurring"


class DayOfWeekCallbackData(CallbackData, prefix='day_of_week'):
    action: ReminderAction
    day: DayOfWeek = None
    selected: bool = False
