from aiogram import Bot, Router, F
from aiogram.filters import or_f
from aiogram.types import Message, CallbackQuery, LabeledPrice

from handlers.show_tasks.show_tasks_kb import choose_task_type_kb, actions_kb
from core.dictionary import *
from database.database import DataBase

show_tasks_router = Router()

@show_tasks_router.message(
    or_f(
        F.text == '/gettasks',
        F.text == f'{start_tasks_text}'
        )
    )
async def choose_task_type(message: Message, bot: Bot):
   await bot.send_message(message.from_user.id, text='Choose, please:', reply_markup=choose_task_type_kb())

@show_tasks_router.callback_query(
    or_f(
        F.data.startswith('ongoing_tasks'),
        F.data.startswith('completed_tasks')
        )
   )
async def get_tasks(call: CallbackQuery):
    db = DataBase()
    tasks = await db.get_tasks(call.data.startswith('completed_tasks'))
    if (tasks):
        for task in tasks:
            await call.message.answer(text=f'•{task.description}')
    else:
        await call.message.answer(f'🚧 No data was found! 🚧')