from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery

from core.dictionary import *
from core.logging_config import logger
from database.database import (
    TaskStatus,
    DataBase
)
from keyboards.task_alteration_kb import *
from keyboards.start_kb import (
    MenuCommandsCallback,
    start_kb
)


router = Router(name=__name__)
db = DataBase()


async def start_command(user_id: int, bot: Bot) -> None:
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
    await callback.answer()
    await start_command(user_id=callback.from_user.id, bot=bot)
    await callback.message.delete()


async def task_type_selection_handler(user_id: int, bot: Bot) -> None:
    await bot.send_message(
        user_id,
        text=task_status_message,
        reply_markup=task_type_kb()
    )
   

@router.message(F.text == MenuCommands.GET_TASKS.value)
async def task_type_selection_command(message: Message, bot: Bot) -> None:
    await task_type_selection_handler(user_id=message.from_user.id, bot=bot)
    await message.delete()


@router.callback_query(
    MenuCommandsCallback.filter(
        F.option == MenuCommands.GET_TASKS
    )
)
async def task_type_selection_callback(callback: CallbackQuery, bot: Bot) -> None:
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
    try:
        callback.answer()
        user = await db.get_user(callback.from_user.id)
        logger.info(f'Task status: {callback_data.type}')
        tasks = await db.get_tasks_by_user(user_id=user.id, status=callback_data.type)
        await callback.message.delete()
        if tasks:
            await callback.message.answer(
                text=f'Tasks:',
                reply_markup=task_list_kb(tasks)
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