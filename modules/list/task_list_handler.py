from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery

from modules.common.commands_callback import (
    MenuCommands,
    MenuCommandsCallback
)
from modules.list.task_list_callback import (
    TaskStatus,
    TaskStatusCallbackData,
)
from database.database import DataBase
from modules.list.task_list_kb import *
from utils.dictionary import *
from utils.logging_config import logger


db = DataBase()
router = Router(name=__name__)


async def handle_task_type_selection(user_id: int, bot: Bot) -> None:
    """
    Sends the task status selection message with the task type keyboard to the user.

    Args:
        user_id (int): The ID of the user.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    try:
        await bot.send_message(
            user_id,
            text=msg_task_status,
            reply_markup=task_type_kb()
        )
    except Exception as error:
        logger.error(f'Error: handle_task_type_selection(): {error}')
   

@router.message(F.text == MenuCommands.GET_TASKS.value)
async def handle_task_type_selection_command(message: Message, bot: Bot) -> None:
    """
    Handles the task type selection command from the user.

    Args:
        message (Message): The message instance.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    try:
        await message.delete()
        await handle_task_type_selection(user_id=message.from_user.id, bot=bot)
    except Exception as error:
        logger.error(f'Error: handle_task_type_selection_command(): {error}')


@router.callback_query(
    MenuCommandsCallback.filter(
        F.option == MenuCommands.GET_TASKS
    )
)
async def handle_task_type_selection_callback(callback: CallbackQuery, bot: Bot) -> None:
    """
    Handles the task type selection callback query.

    Args:
        callback (CallbackQuery): The callback query instance.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    try:
        await callback.answer()
        await callback.message.delete()
        await handle_task_type_selection(user_id=callback.from_user.id, bot=bot)
    except Exception as error:
        logger.error(f'Error: handle_task_type_selection_callback(): {error}')


@router.callback_query(
        TaskStatusCallbackData.filter(
            F.type.in_(TaskStatus)
        )
)
async def handle_task_list(
    callback: CallbackQuery,
    callback_data: TaskStatusCallbackData
) -> None:
    """
    Handles the task list callback query.

    Args:
        callback (CallbackQuery): The callback query instance.
        callback_data (TaskStatusCallbackData): The task status callback data.

    Returns:
        None
    """
    try:
        await callback.answer()
        await callback.message.delete()
        user = await db.get_user(callback.from_user.id)
        tasks = await db.get_all_tasks_by_user(user_id=user.id, status=callback_data.type)
        
        # Reverse the list to show the latest tasks first.
        tasks = tasks[::-1]
        if tasks:
            await callback.message.answer(
                text=f'Tasks:',
                reply_markup=task_list_kb(
                    tasks=tasks,
                    current_page=callback_data.page,
                    task_status=callback_data.type
                )
            )
        else:
            await callback.message.answer(
                text=(f'{msg_task_void}\n\n{msg_task_status}'),
                reply_markup=task_type_kb()
            )
    except Exception as error:
        logger.error(f'Error: handle_task_list(): {error}')