from aiogram.fsm.state import StatesGroup, State

class CreateState(StatesGroup):
    description_task = State()
    reminder_type = State()
    reminder_call = State()
    final_confirmation = State()
