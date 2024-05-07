from aiogram import Bot, Router, F
from aiogram.filters import or_f
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from datetime import datetime

from database.database import DataBase
from core.dictionary import *
from handlers.create_task.create_task_kb import cancel_kb
from handlers.start.start_kb import start_kb
from handlers.create_task.create_task_state import CreateState

create_task_router = Router()


@create_task_router.message(F.text.lower()=='cancel')
async def cmd_cancel(message: Message, state: FSMContext, bot: Bot):
    """
        Clears component's state and
        returns to the start keyborad
    """
    await state.clear()
    await bot.send_message(message.from_user.id, cmd_cancel_create_task, reply_markup=start_kb())


@create_task_router.message(
        or_f(
            F.text == '/createtask',
            F.text == f'{NEW_TASK}'
            )
        )
async def create_task(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Write your task\'s description', reply_markup=cancel_kb)
    await state.set_state(CreateState.description_task)


@create_task_router.message(CreateState.description_task)
async def input_description_task(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(description_task=message.text)
    
    task = await state.get_data()
    try:
        db = DataBase()
        user = await  db.get_user(message.from_user.id)
        await db.add_task( 
                          task['description_task'], 
                          datetime.today(), 
                          user.id
                        )
        await bot.send_message(message.from_user.id, task_creation_completed, reply_markup=None)
    except Exception as error:
        print(f'Database Insertion Error: {error}')
        await bot.send_message(message.from_user.id, task_creation_error, reply_markup=None)
    finally:
        await state.clear()
