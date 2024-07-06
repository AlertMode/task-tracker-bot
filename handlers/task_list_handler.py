from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery

from utils.dictionary import *
from utils.logging_config import logger
from database.database import DataBase
from callbacks.general_commands_callback import (
    MenuCommands,
    MenuCommandsCallback
)
from callbacks.task_list_callback import (
    TaskStatus,
    TaskStatusCallbackData,
)
from keyboards.task_list_kb import *
from keyboards.start_kb import start_kb
from handlers.task_alteration_handler import router as task_alteration_router


db = DataBase()
router = Router(name=__name__)
router.include_router(task_alteration_router)


async def handle_start(user_id: int, bot: Bot) -> None:
    """
    Sends the start message with the start keyboard to the user.

    Args:
        user_id (int): The ID of the user.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    await bot.send_message(
        user_id,
        text=start_message,
        reply_markup=start_kb()
    )
    

@router.callback_query(
        MenuCommandsCallback.filter(
            F.option == MenuCommands.START
        )
)
async def handle_start_callback(
    callback: CallbackQuery,
    bot: Bot
) -> None:
    """
    Handles the start callback query.

    Args:
        callback (CallbackQuery): The callback query instance.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    await callback.answer()
    await handle_start(user_id=callback.from_user.id, bot=bot)
    await callback.message.delete()


async def handle_task_type_selection(user_id: int, bot: Bot) -> None:
    """
    Sends the task status selection message with the task type keyboard to the user.

    Args:
        user_id (int): The ID of the user.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    await bot.send_message(
        user_id,
        text=task_status_message,
        reply_markup=task_type_kb()
    )
   

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
    await handle_task_type_selection(user_id=message.from_user.id, bot=bot)
    await message.delete()


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
    await callback.answer()
    await handle_task_type_selection(user_id=callback.from_user.id, bot=bot)
    await callback.message.delete()


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
        user = await db.get_user(callback.from_user.id)
        tasks = await db.get_tasks_by_user(user_id=user.id, status=callback_data.type)
        await callback.message.delete()
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
                text=(f'{task_void_message}\n\n{task_status_message}'),
                reply_markup=task_type_kb()
            )
    except Exception as error:
        logger.error(f'Error: tasks_list_handler(): {error}')