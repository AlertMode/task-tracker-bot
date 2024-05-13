from aiogram import Bot, Router, F
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.show_tasks.show_tasks_kb import *
from core.dictionary import *
from database.database import DataBase
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
   await bot.send_message(message.from_user.id, text='Please, make a choice:', reply_markup=choose_task_type_kb())


@show_tasks_router.message(F.text == ONGOING_TASKS)
async def get_ongoing_tasks_handler(message: Message, bot: Bot) -> None:
    user = await db.get_user(message.from_user.id)
    tasks = await db.get_tasks(user_id=user.id, areCompleted=False)
    if (tasks):
        for task in tasks:
            await bot.send_message(
                message.from_user.id,
                text=task_ongoing % (
                    task.creation_date,
                    task.description
                ),
                reply_markup=ongoing_tasks_actions_kb(task.id)
            )
    else:
        await bot.send_message(message.from_user.id, text=no_tasks_message)


@show_tasks_router.message(F.text == COMPLETED_TASKS)
async def get_completed_tasks_handler(message: Message, bot: Bot) -> None:
    user = await db.get_user(message.from_user.id)
    tasks = await db.get_tasks(user_id=user.id, areCompleted=True)
    if (tasks):
        for task in tasks:
            await bot.send_message(
                message.from_user.id,
                text=task_completed % (
                    task.creation_date,
                    task.description,
                    task.completion_date
                ),
                reply_markup=completed_tasks_actions_kb(task.id)
            )
    else:
        await bot.send_message(message.from_user.id, text=no_tasks_message)


@show_tasks_router.callback_query(
    or_f(
        F.data.startswith('task_done_'),
        F.data.startswith('task_undone_'),
        F.data.startswith('task_delete_')
    )
)
async def task_actions_handler(callback: CallbackQuery) -> None:
    user = await db.get_user(callback.from_user.id)
    task_id = callback.data.split('_')[-1]
    message = None

    try:
        if (callback.data.startswith('task_done_')):
            await db.set_task_done(user_id=user.id, task_id=task_id)
            message = task_setting_done_completed
        elif (callback.data.startswith('task_undone_')):
            await db.set_task_undone(user_id=user.id, task_id=task_id)
            message = task_setting_undone_completed
        elif (callback.data.startswith('task_delete_')):
            await db.delete_task(user_id=user.id, task_id=task_id)
            message = task_deletion_completed
        
        await callback.message.answer(message)

    except Exception as error:
        print(f'Database Query Error: {error}')
        await callback.message.answer(error_message)   