from aiogram.fsm.state import StatesGroup, State

class CreateState(StatesGroup):
    description_task = State()
    final_confirmation = State()
    