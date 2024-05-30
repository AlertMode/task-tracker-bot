from enum import Enum

from aiogram.filters.callback_data import CallbackData


class MenuCommands(Enum):
    START = '/start'
    CREATE_TASK = '/create_task'
    GET_TASKS = '/get_tasks'


class MenuCommandsCallback(CallbackData, prefix='main_menu'):
    option: MenuCommands