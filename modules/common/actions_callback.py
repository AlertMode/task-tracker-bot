
from enum import (
    IntEnum,
    auto
)

from aiogram.filters.callback_data import CallbackData


class CommonAction(IntEnum):
    TOGGLE = auto()
    CONFIRM = auto()
    CANCEL = auto()
    BACK = auto()
    SKIP = auto()


class CommonActionCallbackData(CallbackData, prefix='common_action'):
    action: CommonAction