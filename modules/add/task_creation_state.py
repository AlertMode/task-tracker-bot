from aiogram.fsm.state import StatesGroup, State

class CreateState(StatesGroup):
    description_task = State()
    reminder_type = State()
    reminderd_reccuring_days = State()
    reminder_single_date = State()
    reminder_time = State()
    final_confirmation = State()
