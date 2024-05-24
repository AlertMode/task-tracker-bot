from aiogram import Bot, Router, F
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.dictionary import *
from database.database import (
    TaskStatus,
    DataBase
)
from keyboards.task_alteration_kb import *
from keyboards.start_kb import MenuCommandsCallback



router = Router(name=__name__)
db = DataBase()


async def task_type_selection_handler(user_id: int, bot: Bot) -> None:
    await bot.send_message(
        user_id,
        text='Select the task status:',
        reply_markup=task_type_kb()
    )
   

@router.callback_query(F.text == MenuCommands.GET_TASKS.value)
async def task_type_selection_command(message: Message, bot: Bot) -> None:
    await task_type_selection_handler(message.from_user.id, bot)
    await message.delete()


@router.callback_query(
    MenuCommandsCallback.filter(
        F.action == MenuCommands.GET_TASKS
    )
)
async def task_type_selection_callback(callback: CallbackQuery, bot: Bot) -> None:
    await task_type_selection_handler(callback.from_user.id, bot)
    await callback.answer()
    await callback.message.delete()


@router.callback_query(
        TaskStatusCallbackData.filter(
            F.type.in_(TaskStatus)
        )
)
async def tasks_list_handler(
    callback: CallbackQuery,
    callback_data: TaskStatusCallbackData
) -> None:
    user = await db.get_user(callback.from_user.id)
    task_status = TaskStatus.COMPLETED if callback_data.type == TaskStatus.COMPLETED else TaskStatus.ONGOING
    print(task_status)
    
    try:
        tasks = await db.get_tasks(user_id=user.id, status=task_status)
        if tasks:
            for task in tasks:
                await callback.message.answer(
                    text=(task_completed
                          if task_status == TaskStatus.COMPLETED
                          else task_ongoing) % (
                                task.creation_date,
                                task.description,
                                task.completion_date
                            ),
                    reply_markup=task_completed_kb(task.id)
                        if task_status == TaskStatus.COMPLETED
                        else task_ongoing_kb(task.id)
                )
        else:
            await callback.message.answer(callback.from_user.id, text=task_void_message)
    except Exception as error:
        print(f'Error: tasks_list_handler(): {error}')


@router.callback_query(
        TaskAlterationCallbackData.filter(
            F.action.in_(TaskAlterationAction)
        )
)
async def task_actions_handler(
    callback: CallbackQuery,
    callback_data: TaskAlterationCallbackData
) -> None:
    user = await db.get_user(callback.from_user.id)
    task_id = callback_data.id
    message = None

    try:
        if (callback_data.action == TaskAlterationAction.done):
            await db.set_task_done(user_id=user.id, task_id=task_id)
            message = task_setting_done_completed
        elif (callback_data.action == TaskAlterationAction.undone):
            await db.set_task_undone(user_id=user.id, task_id=task_id)
            message = task_setting_undone_completed
        elif (callback_data.action == TaskAlterationAction.delete):
            await db.delete_task(user_id=user.id, task_id=task_id)
            message = task_deletion_completed
        
        await callback.message.answer(message)
    except Exception as error:
        print(f'Database Query Error: {error}')
        await callback.message.answer(error_message)