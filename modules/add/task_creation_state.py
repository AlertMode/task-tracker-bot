from aiogram.fsm.state import StatesGroup, State

class CreateTaskState(StatesGroup):
    description = State()
    date = State()
    time_zone = State()
    time_picker = State()
    final_confirmation = State()
