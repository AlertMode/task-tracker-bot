from enum import (
    Enum,
    StrEnum
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


class ReminderInterval(Enum):
    BY_DAYS = 'BY DAYS'
    BY_WEEKS = 'BY WEEKS'
    BY_MONTHS = 'BY MONTHS'
    BY_YEARS = 'BY YEARS'


class ReminderDayCallbackData(CallbackData, prefix='reminder_day'):
    day: DayOfWeek = None
    selected: bool = False


class ReminderIntervalCallbackData(CallbackData, prefix='reminder_interval'):
    interval: ReminderInterval