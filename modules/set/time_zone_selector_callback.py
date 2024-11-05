from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


class TimeZone(StrEnum):
    UTC0 = '+0'
    UTC1 = '+1'
    UTC2 = '+2'
    UTC3 = '+3'
    UTC4 = '+4'
    UTC5 = '+5'
    UTC6 = '+6'
    UTC7 = '+7'
    UTC8 = '+8'
    UTC9 = '+9'
    UTC10 = '+10'
    UTC11 = '+11'
    UTC12 = '+12'
    UTC13 = '+13'
    UTC14 = '+14'
    UTC_1 = '-1'
    UTC_2 = '-2'
    UTC_3 = '-3'
    UTC_4 = '-4'
    UTC_5 = '-5'
    UTC_6 = '-6'
    UTC_7 = '-7'
    UTC_8 = '-8'
    UTC_9 = '-9'
    UTC_10 = '-10'
    UTC_11 = '-11'
    UTC_12 = '-12'
    UTC_13 = '-13'
    UTC_14 = '-14'


class TimeZoneSelectorCallbackData(CallbackData, prefix='time_zone_selector'):
    time_zone: TimeZone