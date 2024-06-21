from aiogram.fsm.state import StatesGroup, State

class CreateState(StatesGroup):
    description_task = State()
    single_reminder = State()
    recurring_reminder = State()
