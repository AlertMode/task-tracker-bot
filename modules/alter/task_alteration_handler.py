from aiogram import Router, F
from aiogram.types import CallbackQuery

from modules.alter.task_alteration_callback import (
    TaskAlterationAction,
    TaskAlterationCallbackData
)
from database.database import DataBase
from modules.list.task_list_kb import *
from modules.alter.task_alteration_kb import *
from utils.dictionary import *
from utils.logging_config import logger


db = DataBase()
router = Router(name=__name__)


@router.callback_query(
    TaskAlterationCallbackData.filter(
        F.action == TaskAlterationAction.SKIP
    )
)
async def handle_task_information(
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
        await callback.answer()
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
        logger.error(f'get_task_information(): {error}')


@router.callback_query(
        TaskAlterationCallbackData.filter(
            F.action != TaskAlterationAction.SKIP
        )
)
async def handle_task_information_alteration(
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
    try:
        await callback.answer()
        user = await db.get_user(callback.from_user.id)
        task_id = callback_data.id
        message = None

        if (callback_data.action == TaskAlterationAction.DONE):
            await db.set_task_done(user_id=user.id, task_id=task_id)
            message = task_setting_done_completed
        elif (callback_data.action == TaskAlterationAction.UNDONE):
            await db.set_task_undone(user_id=user.id, task_id=task_id)
            message = task_setting_undone_completed
        elif (callback_data.action == TaskAlterationAction.DELETE):
            await db.delete_task(user_id=user.id, task_id=task_id)
            message = task_deletion_completed
        
        tasks = await db.get_all_tasks_by_user(
            user_id=user.id,
            status=callback_data.status
        )

        await callback.message.answer(
            text=(f'{message}\n\n{task_status_message}'),
            reply_markup= task_list_kb(
                tasks=tasks,
                current_page=0,
                task_status=callback_data.status,
                from_the_end=True
            ) if tasks else task_type_kb()
        )
        await callback.message.delete()
    except Exception as error:
        logger.error(f'Database Query Error: {error}')
        await callback.message.answer(error_message)