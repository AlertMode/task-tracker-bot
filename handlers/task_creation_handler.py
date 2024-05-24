from aiogram import Bot, Router, F
from aiogram.filters import or_f
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from datetime import datetime

from database.database import DataBase
from core.dictionary import *
from keyboards.task_creation_kb import return_to_main_menu_kb
from keyboards.start_kb import start_kb
from states.task_creation_state import CreateState


router = Router(name=__name__)


@router.message(F.text==MainMenuReplyKeyboard.MAIN_MENU)
async def return_to_main_menu_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    """
        Clears component's state and
        returns to the start keyborad
    """
    await state.clear()
    await bot.send_message(
        message.from_user.id,
        task_creation_cancel_cmd,
        reply_markup=start_kb()
    )


@router.message(
        or_f(
            F.text == MenuCommands.CREATE_TASK,
            F.text == MainMenuReplyKeyboard.NEW_TASK
            )
        )
async def create_task(message: Message, state: FSMContext, bot: Bot) -> None:
    await bot.send_message(
        message.from_user.id,
        task_creation_description_prompt,
        reply_markup=return_to_main_menu_kb
    )
    await state.set_state(CreateState.description_task)


@router.message(CreateState.description_task, F.text)
async def input_description_task(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(description_task=message.text)
    
    task = await state.get_data()
    try:
        db = DataBase()
        user = await db.get_user(message.from_user.id)
        await db.add_task(
            task['description_task'], 
            datetime.today(), 
            user.id
        )
        await bot.send_message(
            message.from_user.id,
            task_creation_completed,
            reply_markup=None
        )
    except Exception as error:
        await bot.send_message(
            message.from_user.id,
            error_message,
            reply_markup=None
        )
    finally:
        await state.clear()


@router.message(CreateState.description_task)
async def input_description_task_invalid_content_type(message: Message, bot: Bot) -> None:
    await bot.send_message(
        message.from_user.id,
        task_createion_invalid_content_type
    )