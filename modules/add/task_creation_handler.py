from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram3_calendar import SimpleCalendar
from aiogram3_calendar.calendar_types import SimpleCalendarCallback

from database.database import DataBase
from modules.add.task_creation_callback import *
from modules.add.task_creation_kb import *
from modules.add.task_creation_state import CreateState
from modules.common.auxilary_handler import *
from modules.common.commands_callback import (
    MenuCommands,
    MenuCommandsCallback
)
from modules.list.task_list_callback import TaskStatus
from modules.list.task_list_kb import task_list_kb
from modules.set.time_zone_selector_handler import router as time_zone_selector_router
from modules.set.time_zone_selector_kb import create_time_zone_keyboard
from modules.start.start_kb import start_kb
from utils.dictionary import *


router = Router(name=__name__)
router.include_router(time_zone_selector_router)


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
        await bot.send_message(
            chat_id=user_id,
            text=msg_task_creation_description_prompt,
            reply_markup=return_to_main_menu_kb
        )
        await state.clear()
        await state.set_state(CreateState.description)
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
    try:
        message.delete()
        await handle_task_creation(
            user_id = message.from_user.id,
            state=state,
            bot=bot
        )
    except Exception as error:
        logger.error(f"create_task_command: {error}")


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
    try:
        await callback.answer()
        await callback.message.delete()
        await handle_task_creation(
            user_id=callback.from_user.id,
            state=state,
            bot=bot    
        )
    except Exception as error:
        logger.error(f"create_task_callback: {error}")
    

@router.message(CreateState.description, F.text)
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
        await message.delete()
        await state.update_data(description_task=message.text)
        await state.set_state(CreateState.date)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=msg_date_selection,
            reply_markup = await SimpleCalendar().start_calendar()
        )
    except Exception as error:
        logger.error(f"handle_task_description_input: {error}")
        await state.clear()


@router.message(CreateState.description)
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
    SimpleCalendarCallback.filter()
)
async def handle_simple_calendar_date_selection(
    callback: CallbackQuery,
    callback_data: dict,
    state: FSMContext
) -> None:
    try:
        await callback.answer()
        selected, date = await SimpleCalendar().process_selection(callback, callback_data)
        if selected:
            await state.update_data(date = date)
            await state.set_state(CreateState.time_zone)
            await callback.message.delete()
            await callback.message.answer(
                text=task_reminder_timezone,
                reply_markup=create_time_zone_keyboard()
            )
    except Exception as error:
        logger.error(f"handle_simple_calendar_date_selection: {error}")
        await state.clear()


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
            reminder_date=task['date']
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
            chat_id=callback.from_user.id,
            text=error_message,
            reply_markup=None
        )
    finally:
        await state.clear()