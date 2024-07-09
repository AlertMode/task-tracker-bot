from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message
)

from modules.add.task_creation_callback import *
from modules.add.task_creation_state import CreateState
from utils.dictionary import *
from utils.logging_config import logger


router = Router(name=__name__)


@router.callback_query(
    CreateState.reminder_type,
    ReminderTypeCallbackData.filter(
        F.type == ReminderType.SINGLE
    )
)
async def handle_single_reminder_listener(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
#TODO: Implement the handler for the single reminder listener,
# using external calendar keyboard package.
    try:
        pass
    except Exception as error:
        logger.error(f"handle_single_reminder_listener: {error}")