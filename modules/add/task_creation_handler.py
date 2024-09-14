from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery
)

from modules.common.commands_callback import (
    MenuCommands,
    MenuCommandsCallback
)
from modules.add.task_creation_callback import *
from modules.list.task_list_callback import TaskStatus
from database.database import DataBase
from modules.common.auxilary_handler import *
from modules.set.reminder_recurrig_handler import router as recurring_reminder_router
from modules.start.start_kb import start_kb
from modules.add.task_creation_kb import *
from modules.list.task_list_kb import task_list_kb
from modules.add.task_creation_state import CreateState
from utils.dictionary import *


router = Router(name=__name__)
router.include_router(recurring_reminder_router)


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
    await bot.send_message(
        chat_id=message.from_user.id,
        text=mag_task_creation_cancel_cmd,
        reply_markup=start_kb()
    )
    await store_message_id(state=state, message_id=message.message_id)
    await delete_all_messages(state=state, bot=bot, chat_id=message.from_user.id)
    await state.clear()


async def handle_task_creation(
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
    try:
        response = await bot.send_message(
            chat_id=user_id,
            text=msg_task_creation_description_prompt,
            reply_markup=return_to_main_menu_kb
        )
        await state.clear()
        await delete_all_messages(state=state, bot=bot, chat_id=user_id)
        await state.set_state(CreateState.description_task)
        await store_message_id(state=state, message_id=response.message_id)
    except Exception as error:
        logger.error(f"handle_task_creation: {error}")


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
    await handle_task_creation(
        user_id = message.from_user.id,
        state=state,
        bot=bot
    )
    await store_message_id(state=state, message_id=message.message_id)


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
    await handle_task_creation(
        user_id=callback.from_user.id,
        state=state,
        bot=bot    
    )
    await callback.answer()
    await store_message_id(state=state, message_id=callback.message.message_id)
    

@router.message(CreateState.description_task, F.text)
async def handle_task_description_input(
    message: Message,
    bot: Bot,
    state: FSMContext
) -> None:
    """
    Handles the input of the task description.

    Args:
        message (Message): The incoming message object.
        state (FSMContext): The FSM context object.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    try:
        await delete_all_messages(
            state=state,
            bot=bot,
            chat_id=message.from_user.id
        )
        await state.update_data(description_task=message.text)
        await state.set_state(CreateState.reminder_type)
        await store_message_id(state=state, message_id=message.message_id)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=task_reminder_type_selection,
            reply_markup=reminder_type_selection_kb() 
        )
        await message.delete()
    except Exception as error:
        logger.error(f"handle_task_description_input: {error}")
        await state.clear()


@router.message(CreateState.description_task)
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
        logger.error(f"handle_invalid_description_content_type: {error}")
        

@router.callback_query(
        CommonActionCallbackData.filter(
            F.action == CommonAction.SKIP
        ),
        # Filter the CommonActionCallbackData to the reminder type state.
        # In order to prevent the callback from being called in other states
        # or by other similar callback data.
        CreateState()
)
@router.callback_query(
    CreateState.final_confirmation,
    CommonActionCallbackData.filter(
            F.action == CommonAction.CONFIRM
        )
)
async def handle_final_confirmation(
    message: Message,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    Handles the final confirmation of the task creation and writes to the database.

    Args:
        message (Message): The incoming message object.
        state (FSMContext): The FSM context object.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    try:
        task = await state.get_data()
        db = DataBase()
        user = await db.get_user(message.from_user.id)

        reminder_date = None
        selected_days = None
        if task['reminder_type'] == ReminderType.RECURRING:
            reminder_date = task['next_reminder_date']
            selected_days = task['selected_days']

        await db.add_task(
            description=task['description_task'],
            creation_date=datetime.today(),
            user_id=user.id,
            reminder_date=reminder_date,
            recurring_days=selected_days
        )

        tasks = await db.get_all_tasks_by_user(
            user_id=user.id,
            status=TaskStatus.ONGOING  
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text=msg_task_creation_completed % task['description_task'],
            reply_markup=task_list_kb(
                tasks=tasks,
                current_page=0,
                task_status=TaskStatus.ONGOING,
                from_the_end=True
            )
        )
    except Exception as error:
        logger.error(f'handle_final_confirmation: {error}')
        await bot.send_message(
            chat_id=message.from_user.id,
            text=error_message,
            reply_markup=None
        )
    finally:
        await state.clear()