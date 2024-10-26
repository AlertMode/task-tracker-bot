from aiogram.fsm.state import StatesGroup, State


class AlterTaskState(StatesGroup):
    edit_description = State()
    edit_date = State()
    edit_time_zone = State()
    edit_time = State()