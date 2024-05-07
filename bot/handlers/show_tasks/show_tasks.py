from aiogram import Bot, Router, F
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

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
   await bot.send_message(message.from_user.id, text='Choose, please:', reply_markup=choose_task_type_kb())


@show_tasks_router.message(F.text == ONGOING_TASKS)
async def get_ongoing_tasks_handler(message: Message, bot: Bot) -> None:
    tasks = await db.get_tasks(areCompleted=False)
    if (tasks):
        for task in tasks:
            await bot.send_message(message.from_user.id, text=task_ongoing % (task.creation_date, task.description))
    else:
        await bot.send_message(message.from_user.id, text=no_tasks_message)


@show_tasks_router.message(F.text == COMPLETED_TASKS)
async def get_completed_tasks_handler(message: Message, bot: Bot) -> None:
    tasks = await db.get_tasks(areCompleted=True)
    if (tasks):
        for task in tasks:
            await bot.send_message(message.from_user.id, text=task_completed % (task.creation_date, task.description, task.completion_date))
    else:
        await bot.send_message(message.from_user.id, text=no_tasks_message)
