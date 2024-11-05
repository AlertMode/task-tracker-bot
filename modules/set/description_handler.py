from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram3_calendar import SimpleCalendar

from database.database import DataBase
from modules.list.task_list_kb import *
from modules.add.task_creation_state import CreateTaskState
from modules.alter.task_alteration_kb import *
from modules.alter.task_alteration_state import AlterTaskState
from modules.set.calendar_handler import router as calendar_handler_router
from utils.dictionary import *
from utils.logging_config import logger


router = Router(name=__name__)
router.include_router(calendar_handler_router)


@router.message(CreateTaskState.description, F.text)
@router.message(AlterTaskState.edit_description, F.text)
async def handle_description_input(
    message: Message,
    bot: Bot,
    state: FSMContext
) -> None:
    """
    Handles the description input.

    Args:
        message (Message): The incoming message object.
        bot (Bot): The bot instance.
        state (FSMContext): The state machine context.

    Returns:
        None
    """
    try:
        db = DataBase()
        current_state = await state.get_state()

        await message.delete()
        if current_state == CreateTaskState.description.state:
            await state.update_data(description_task=message.text)
            await state.set_state(CreateTaskState.date)

            await bot.send_message(
                chat_id=message.from_user.id,
                text=msg_date_selection,
                reply_markup = await SimpleCalendar().start_calendar()
            )

        elif current_state == AlterTaskState.edit_description.state:
            task_id = (await state.get_data()).get('task_id')
            await db.edit_task_description(
                task_id=task_id,
                new_description=message.text
            )
            await state.clear()

            await bot.send_message(
                chat_id=message.from_user.id,
                text=(f'{msg_task_description_change_completed}\n\n{message.text}'),
                reply_markup = task_edit_kb(task_id)
            )        

    except Exception as error:
        logger.error(f'handle_description_input: {error}')
        await message.answer(msg_error)
        await state.clear()


@router.message(CreateTaskState.description)
@router.message(AlterTaskState.edit_description)
async def handle_invalid_description_content_type(
    message: Message,
    bot: Bot
) -> None:
    """
    Handles the invalid content type for the task description.

    Args:
        message (Message): The incoming message object.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    try:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=msg_task_createion_invalid_content_type,
            reply_markup=None
        )
    except Exception as error:
        logger.error(f'handle_invalid_description_content_type: {error}')