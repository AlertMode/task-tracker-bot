from aiogram.fsm.state import StatesGroup, State

class CreateState(StatesGroup):
    description_task = State()
    reminder_type = State()
    reminder_single_date = State()
    reminderd_reccuring_date = State()
    reminder_interval_type = State()
    reminder_interval_number = State()
    reminder_time = State()
    final_confirmation = State()
