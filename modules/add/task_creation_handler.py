from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery
)

from database.database import DataBase
from modules.add.task_creation_callback import *
from modules.add.task_creation_kb import *
from modules.add.task_creation_state import CreateTaskState
from modules.common.auxilary_handler import *
from modules.common.commands_callback import (
    MenuCommands,
    MenuCommandsCallback
)
from modules.list.task_list_callback import TaskStatus
from modules.start.start_kb import start_kb
from utils.dictionary import *


router = Router(name=__name__)


@router.message(F.text==MenuNames.MAIN_MENU)
@router.callback_query(
    CommonActionCallbackData.filter(
        F.action == CommonAction.CANCEL
    )
)
async def return_to_main_menu_handler(
    message: Message,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    Handler function to return to the main menu.

    Args:
        message (Message): The incoming message object.
        state (FSMContext): The state machine context.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    try:
        await state.clear()
        await bot.send_message(
            chat_id=message.from_user.id,
            text=mag_task_creation_cancel_cmd,
            reply_markup=start_kb()
        )
    except Exception as error:
        logger.error(f"return_to_main_menu_handler: {error}")

@router.message(F.text == MenuCommands.CREATE_TASK.value)
@router.callback_query(
        MenuCommandsCallback.filter(
            F.option == MenuCommands.CREATE_TASK
        )
)
async def handle_task_creation(
        answer: CallbackQuery | Message,
        state: FSMContext,
        bot: Bot
) -> None:
    """
    Handles the creation of a new task.

    Args:
        user_id (int): The ID of the user creating the task.
        state (FSMContext): The state of the conversation.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    try:
        if isinstance(answer, CallbackQuery):
            await answer.answer()
            await answer.message.delete()
        elif isinstance(answer, Message):
            await answer.delete()

        await bot.send_message(
            chat_id=answer.from_user.id,
            text=msg_task_creation_description_prompt,
            reply_markup=return_to_main_menu_kb
        )
        await state.clear()
        await state.set_state(CreateTaskState.description)
    except Exception as error:
        logger.error(f"handle_task_creation: {error}")


@router.callback_query(
        CommonActionCallbackData.filter(
            F.action == CommonAction.SKIP
        ),
        # Filter the CommonActionCallbackData to the reminder type state.
        # In order to prevent the callback from being called in other states
        # or by other similar callback data.
        CreateTaskState()
)
@router.callback_query(
    CreateTaskState.final_confirmation,
    CommonActionCallbackData.filter(
            F.action == CommonAction.CONFIRM
        )
)
async def handle_final_confirmation(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    Handles the final confirmation of the task creation and writes to the database.

    Args:
        callback (CallbackQuery): The callback query object.
        state (FSMContext): The FSM context object.
        bot (Bot): The bot object.

    Returns:
        None
    """
    try:
        task = await state.get_data()
        db = DataBase()
        user = await db.get_user(callback.from_user.id)

        await db.add_task(
            description=task['description_task'],
            creation_date=datetime.today(),
            user_id=user.id,
            reminder_date=task['date'],
            reminder_utc=task['time_zone']
        )

        tasks = await db.get_all_tasks_by_user(
            user_id=user.id,
            status=TaskStatus.ONGOING  
        )
        await callback.answer()
        await callback.message.delete()
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=msg_task_creation_completed % task['description_task'],
            reply_markup=None
        )
    except Exception as error:
        logger.error(f'handle_final_confirmation: {error}')
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=msg_error,
            reply_markup=None
        )
    finally:
        await state.clear()