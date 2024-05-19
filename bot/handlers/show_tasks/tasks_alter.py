from aiogram import Bot, Router, F
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.show_tasks.tasks_alter_kb import *
from core.dictionary import *
from database.database import (
    TaskStatus,
    DataBase
)
from handlers.start.start_kb import start_kb

show_tasks_router = Router()
db = DataBase()


@show_tasks_router.message(
    or_f(
        F.text == '/gettasks',
        F.text == f'{GET_TASKS}'
        )
    )
async def choose_task_type(message: Message, bot: Bot) -> None:
   await bot.send_message(message.from_user.id,
                          text='Please, make a choice:',
                          reply_markup=task_choose_type_kb())


@show_tasks_router.message(
        or_f(
            F.text == ONGOING_TASKS,
            F.text == COMPLETED_TASKS
        )
)
async def tasks_list_handler(message: Message, bot: Bot) -> None:
    user = await db.get_user(message.from_user.id)
    task_status = TaskStatus.COMPLETED if message.text == COMPLETED_TASKS else TaskStatus.ONGOING
    print(task_status)
    
    try:
        tasks = await db.get_tasks(user_id=user.id, status=task_status)
        if tasks:
            for task in tasks:
                await bot.send_message(
                    message.from_user.id,
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
            await bot.send_message(message.from_user.id, text=task_void_message)
    except Exception as error:
        print(f'Error: tasks_list_handler(): {error}')


@show_tasks_router.callback_query(
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