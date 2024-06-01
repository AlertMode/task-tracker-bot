from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery

from utils.dictionary import *
from utils.logging_config import logger
from database.database import (
    TaskStatus,
    DataBase
)
from callbacks.common_commands_callback import (
    MenuCommands,
    MenuCommandsCallback
)
from callbacks.task_alteration_callback import (
    TaskStatus,
    TaskAlterationAction,
    TaskStatusCallbackData,
    TaskAlterationCallbackData
)
from keyboards.task_alteration_kb import *
from keyboards.start_kb import start_kb


router = Router(name=__name__)
db = DataBase()


async def start_handler(user_id: int, bot: Bot) -> None:
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
async def start_callback(
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
    await start_handler(user_id=callback.from_user.id, bot=bot)
    await callback.message.delete()


async def task_type_selection_handler(user_id: int, bot: Bot) -> None:
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
async def task_type_selection_command(message: Message, bot: Bot) -> None:
    """
    Handles the task type selection command from the user.

    Args:
        message (Message): The message instance.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    await task_type_selection_handler(user_id=message.from_user.id, bot=bot)
    await message.delete()


@router.callback_query(
    MenuCommandsCallback.filter(
        F.option == MenuCommands.GET_TASKS
    )
)
async def task_type_selection_callback(callback: CallbackQuery, bot: Bot) -> None:
    """
    Handles the task type selection callback query.

    Args:
        callback (CallbackQuery): The callback query instance.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    await callback.answer()
    await task_type_selection_handler(user_id=callback.from_user.id, bot=bot)
    await callback.message.delete()


@router.callback_query(
        TaskStatusCallbackData.filter(
            F.type.in_(TaskStatus)
        )
)
async def task_list_handler(
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
        callback.answer()
        user = await db.get_user(callback.from_user.id)
        logger.info(f'Task status: {callback_data.type}')
        tasks = await db.get_tasks_by_user(user_id=user.id, status=callback_data.type)
        await callback.message.delete()
        if tasks:
            await callback.message.answer(
                text=f'Tasks:',
                reply_markup=task_list_kb(tasks, current_page=callback_data.page)
            )
        else:
            await callback.message.answer(
                text=(f'{task_void_message}\n\n{task_status_message}'),
                reply_markup=task_type_kb()
            )
    except Exception as error:
        logger.error(f'Error: tasks_list_handler(): {error}')


@router.callback_query(
        TaskAlterationCallbackData.filter(
            F.action == TaskAlterationAction.SKIP
        )
)
async def task_full_information_handler(
    callback: CallbackQuery,
    callback_data: TaskAlterationCallbackData
) -> None:
    """
    Handles the task full information callback query.

    Args:
        callback (CallbackQuery): The callback query instance.
        callback_data (TaskAlterationCallbackData): The task alteration callback data.

    Returns:
        None
    """
    try:
        callback.answer()
        task = await db.get_task_by_id(task_id=callback_data.id)
        await callback.message.delete()
        await callback.message.answer(
            text=(task_completed
                if task.completion_date
                else task_ongoing) % (
                    task.creation_date,
                    task.description,
                    task.completion_date
                ),
            reply_markup=task_completed_kb(task.id)
                if task.completion_date
                else task_ongoing_kb(task.id)
        )
    except Exception as error:
        print(f'Error: task_full_information_handler(): {error}')


@router.callback_query(
        TaskAlterationCallbackData.filter(
            F.action != TaskAlterationAction.SKIP
        )
)
async def task_actions_handler(
    callback: CallbackQuery,
    callback_data: TaskAlterationCallbackData
) -> None:
    """
    Handles the task actions callback query (done, undone, delete).

    Args:
        callback (CallbackQuery): The callback query instance.
        callback_data (TaskAlterationCallbackData): The task alteration callback data.

    Returns:
        None
    """
    callback.answer()
    user = await db.get_user(callback.from_user.id)
    task_id = callback_data.id
    message = None

    try:
        if (callback_data.action == TaskAlterationAction.DONE):
            await db.set_task_done(user_id=user.id, task_id=task_id)
            message = task_setting_done_completed
        elif (callback_data.action == TaskAlterationAction.UNDONE):
            await db.set_task_undone(user_id=user.id, task_id=task_id)
            message = task_setting_undone_completed
        elif (callback_data.action == TaskAlterationAction.DELETE):
            await db.delete_task(user_id=user.id, task_id=task_id)
            message = task_deletion_completed
        
        await callback.message.answer(
            text=(f'{message}\n\n{task_status_message}'),
            reply_markup=task_type_kb()
        )
        await callback.message.delete()
    except Exception as error:
        logger.error(f'Database Query Error: {error}')
        await callback.message.answer(error_message)