from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram.fsm.context import FSMContext

from callbacks.common_commands_callback import (
    MenuCommands,
    MenuCommandsCallback
)
from database.database import DataBase
from keyboards.start_kb import start_kb
from keyboards.task_creation_kb import return_to_main_menu_kb
from states.task_creation_state import CreateState
from utils.dictionary import *
from handlers.task_description_handler import *



router = Router(name=__name__)


@router.message(F.text==MenuNames.MAIN_MENU)
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
    await state.clear()
    await bot.send_message(
        message.from_user.id,
        task_creation_cancel_cmd,
        reply_markup=start_kb()
    )


async def create_task_handler(
        user_id: int,
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
    await bot.send_message(
        chat_id=user_id,
        text=task_creation_description_prompt,
        reply_markup=return_to_main_menu_kb
    )
    await state.set_state(CreateState.description_task)


@router.message(F.text == MenuCommands.CREATE_TASK.value)
async def create_task_command(
    message: Message,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    Handles the command to create a new task.

    Args:
        message (Message): The message object representing the command.
        state (FSMContext): The state object for the conversation.
        bot (Bot): The bot object for sending messages.

    Returns:
        None
    """
    await create_task_handler(
        user_id = message.from_user.id,
        state=state,
        bot=bot
    )
    message.delete()


@router.callback_query(
        MenuCommandsCallback.filter(
            F.option == MenuCommands.CREATE_TASK
        )
)
async def create_task_callback(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    Callback function for handling the creation of a task.

    Args:
        callback (CallbackQuery): The callback query object.
        state (FSMContext): The FSM context object.
        bot (Bot): The bot object.

    Returns:
        None
    """
    await create_task_handler(
        user_id=callback.from_user.id,
        state=state,
        bot=bot    
    )
    await callback.answer()
    await callback.message.delete()
    

@router.message(CreateState.description_task, F.text)
async def on_task_description_input(message: Message, state: FSMContext, bot: Bot):
    """
    Handles the input of task description.

    Args:
        message (Message): The message object received from the user.
        state (FSMContext): The FSM context object for managing the conversation state.
        bot (Bot): The bot instance for sending messages.

    Returns:
        None
    """
    await handle_task_description_input(message=message, state=state, bot=bot)


@router.message(CreateState.description_task)
async def on_invalid_description_content_type(message: Message, bot: Bot):
    """
    Handles the case when the description content type is invalid.

    Args:
        message (Message): The incoming message.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    await handle_invalid_description_content_type(message=message, bot=bot)