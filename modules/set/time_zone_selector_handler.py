from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from modules.add.task_creation_state import CreateState
from modules.set.time_picker_handler import router as time_picker_router
from modules.set.time_picker_kb import create_time_picker_keyboard
from modules.set.time_zone_selector_callback import *
from utils.dictionary import *
from utils.logging_config import logger


router = Router(name=__name__)
router.include_router(time_picker_router)


@router.callback_query(
        TimeZoneSelectorCallbackData.filter(),
        CreateState.time_zone
)
async def handle_time_zone_selector(
    callback: CallbackQuery,
    callback_data: TimeZoneSelectorCallbackData,
    state: FSMContext
) -> None:
    """
    Handles the time zone selector callback query.

    Args:
        callback (CallbackQuery): The callback query instance.
        callback_data (TimeZoneSelectorCallbackData): The time zone selector callback data.
        state (FSMContext): The FSM context.

    Returns:
        None
    """
    try:
        selected_time_zone = callback_data.time_zone
        await state.update_data(time_zone=selected_time_zone)

        await state.set_state(CreateState.time_picker)
        await callback.message.answer(
            text=task_reminder_time_picker,
            reply_markup=create_time_picker_keyboard()
        )
        await callback.answer()
        await callback.message.delete()
    except Exception as error:
        logger.error(f"handle_time_zone_selector: {error}")
        await callback.answer("An error occurred while selecting the time zone.")