from aiogram.fsm.state import StatesGroup, State

class CreateState(StatesGroup):
    description = State()
    date = State()
    time_zone = State()
    time_picker = State()
    final_confirmation = State()
