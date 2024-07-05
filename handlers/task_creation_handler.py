from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery
)

from callbacks.general_commands_callback import (
    MenuCommands,
    MenuCommandsCallback
)
from callbacks.task_creation_callback import *
from callbacks.task_list_callback import TaskStatus
from database.database import DataBase
from handlers.auxilary_handler import *
from keyboards.start_kb import start_kb
from keyboards.task_creation_kb import *
from keyboards.task_list_kb import task_list_kb
from states.task_creation_state import CreateState
from utils.dictionary import *


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
    await bot.send_message(
        message.from_user.id,
        task_creation_cancel_cmd,
        reply_markup=start_kb()
    )
    await store_message_id(state=state, message_id=message.message_id)
    await delete_all_messages(state=state, bot=bot, chat_id=message.from_user.id)
    await state.clear()


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
    response = await bot.send_message(
        chat_id=user_id,
        text=task_creation_description_prompt,
        reply_markup=return_to_main_menu_kb
    )
    await delete_all_messages(state=state, bot=bot, chat_id=user_id)
    await state.set_state(CreateState.description_task)
    await store_message_id(state=state, message_id=response.message_id)


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
    await create_task_handler(
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
            text=task_createion_invalid_content_type,
            reply_markup=None
        )
    except Exception as error:
        logger.error(f"handle_invalid_description_content_type: {error}")


@router.callback_query(
    CreateState.reminder_type,
    ReminderTypeCallbackData.filter(
        F.type == ReminderType.RECURRING
    )
)
async def handle_recurring_reminder_selection_keyboardcall(
    callback: CallbackQuery
) -> None:
    try:
        await callback.answer()
        print('FNOENE')
        await callback.message.answer(
            text=task_reminder_message,
            reply_markup=recurring_day_selection_kb(set())
        )
    except Exception as error:
        logger.error(f"handle_recurring_reminder_selection: {error}")


@router.callback_query(
    ReminderDayCallbackData.filter(
        F.selected != None
    )
)
async def handle_recurring_reminder_selection_callback(
    callback: CallbackQuery,
    callback_data: ReminderDayCallbackData,
    state: FSMContext
) -> None:
    try:
        data = await state.get_data()
        selected_days = data.get('selected_days', set())

        #TODO: Fix the issue with the selected_days being updated with delayed data.

        print(
            f"Day: {callback_data.day}, Selected: {callback_data.selected}\n"
            f"description: {data.get('description_task')}\n"
            f"selected_days: {selected_days}\n"
        )

        # Toggle the day selection in the set of selected days for the keybaord.
        if callback_data.day in selected_days:
            selected_days.remove(callback_data.day)
        else:
            selected_days.add(callback_data.day)

        await state.update_data(selected_days=selected_days)

        # Update the keyboard with the new selection.
        new_markup = recurring_day_selection_kb(selected_days)
        await callback.message.edit_reply_markup(
            reply_markup=new_markup
        )

        await callback.answer()
    except Exception as error:
        logger.error(f"handle_recurring_reminder_selection_callback: {error}")


@router.callback_query(CreateState.final_confirmation)
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
        await db.add_task(
            description=task['description_task'],
            creation_date=datetime.today(),
            user_id=user.id
        )

        tasks = await db.get_tasks_by_user(
            user_id=user.id,
            status=TaskStatus.ONGOING  
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text=task_creation_completed % task['description_task'],
            reply_markup=task_list_kb(
                tasks=tasks,
                current_page=0,
                task_status=TaskStatus.ONGOING,
                from_the_end=True
            )
        )
    except Exception as error:
        logger.error(f'Error: handle_task_description_input: {error}')
        await bot.send_message(
            chat_id=message.from_user.id,
            text=error_message,
            reply_markup=None
        )
    finally:
        await state.clear()