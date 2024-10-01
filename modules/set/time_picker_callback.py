from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


class HoursTens(StrEnum):
    ZERO = '0'
    ONE = '1'
    TWO = '2'


class HoursOnes(StrEnum):
    ZERO = '0'
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'


class MinutesTens(StrEnum):
    ZERO = '0'
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'


class MinutesOnes(StrEnum):
    ZERO = '0'
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'


class TimePickerAction(StrEnum):
    CONFIRM = 'confirm'
    ADJUST = 'adjust' 


class TimePickerCallbackData(CallbackData, prefix='time_picker'):
    hours_tens: HoursTens = HoursTens.ZERO
    hours_ones: HoursOnes = HoursOnes.ZERO
    minutes_tens: MinutesTens = MinutesTens.ZERO
    minutes_ones: MinutesOnes = MinutesOnes.ZERO
    action: TimePickerAction = TimePickerAction.ADJUST