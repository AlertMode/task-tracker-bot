from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message
)

from aiogram3_calendar import SimpleCalendar
from aiogram3_calendar.calendar_types import SimpleCalendarCallback

from modules.alter.task_alteration_callback import (
    TaskAlterationAction,
    TaskAlterationCallbackData
)
from database.database import DataBase
from modules.list.task_list_kb import *
from modules.alter.task_alteration_kb import *
from modules.alter.task_alteration_state import AlterTaskState
from modules.set.time_picker_kb import create_time_picker_keyboard
from modules.set.time_zone_selector_kb import create_time_zone_keyboard
from utils.dictionary import *
from utils.logging_config import logger


db = DataBase()
router = Router(name=__name__)


@router.message(F.text==MenuNames.EDIT_MENU)
async def return_to_edit_menu_handler(
    message: Message,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    Handler function to return to the edit menu.

    Args:
        message (Message): The incoming message object.
        state (FSMContext): The state machine context.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    try:
        task_id = (await state.get_data()).get('task_id')
        await state.clear()
        await bot.send_message(
            chat_id=message.from_user.id,
            text=msg_edit_task_description_cancel,
            reply_markup=task_edit_kb(task_id)
        )
    except Exception as error:
        logger.error(f'return_to_edit_menu_handler: {error}')
        await message.answer(error_message)


@router.callback_query(
    TaskAlterationCallbackData.filter(
        F.action == TaskAlterationAction.SELECT
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
            text=(task_completed % (
                    task.creation_date,
                    task.description,
                    task.completion_date
                )
                if task.completion_date
                else task_ongoing
                % (
                    task.creation_date,
                    task.description,
                    task.reminder_date
                )),
            reply_markup=task_completed_kb(task.id)
                if task.completion_date
                else task_ongoing_kb(task.id)
        )
    except Exception as error:
        logger.error(f'handle_task_information(): {error}')


@router.callback_query(
        TaskAlterationCallbackData.filter(
            F.action != TaskAlterationAction.SELECT
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
        await callback.message.delete()
        user = await db.get_user(callback.from_user.id)
        task_id = callback_data.id
        message = None

        if (callback_data.action == TaskAlterationAction.DONE):
            await db.set_task_done(user_id=user.id, task_id=task_id)
            message = msg_task_setting_done_completed
        elif (callback_data.action == TaskAlterationAction.UNDONE):
            await db.set_task_undone(user_id=user.id, task_id=task_id)
            message = msg_task_setting_undone_completed
        elif (callback_data.action == TaskAlterationAction.EDIT):
            await callback.message.answer(
                text=msg_edit_task,
                reply_markup=task_edit_kb(task_id)
            )
            return
        elif (callback_data.action == TaskAlterationAction.DELETE):
            await db.delete_task(user_id=user.id, task_id=task_id)
            message = msg_task_deletion_completed
        
        tasks = await db.get_all_tasks_by_user(
            user_id=user.id,
            status=callback_data.status
        )

        await callback.message.answer(
            text=(f'{message}\n\n{task_status_message}'),
            reply_markup=task_list_kb(
                tasks=tasks,
                current_page=0,
                task_status=callback_data.status,
                from_the_end=True
            ) if tasks else task_type_kb()
        )
    except Exception as error:
        logger.error(f'handle_task_information_alteration: {error}')
        await callback.message.answer(error_message)


@router.callback_query(
    TaskEditCallbackData.filter()
)
async def handle_task_edit(
    callback: CallbackQuery,
    callback_data: TaskEditCallbackData,
    state: FSMContext
) -> None:
    """
    Handles the task edit callback query.

    Args:
        callback (CallbackQuery): The callback query instance.
        callback_data (TaskEditCallbackData): The task edit callback data.

    Returns:
        None
    """
    try:
        await callback.answer()
        await callback.message.delete()

        task = await db.get_task_by_id(task_id=callback_data.id)
        message = None
        reply = None

        if (callback_data.action == TaskEditAction.CHANGE_DESCRIPTION):
            message = task.description
            reply = return_to_edit_menu_kb
            await state.set_state(AlterTaskState.edit_description)
        elif (callback_data.action == TaskEditAction.CHANGE_DATE):
            message = task.reminder_date.strftime('%Y-%m-%d')
            reply = await SimpleCalendar().start_calendar()
            await state.set_state(AlterTaskState.edit_date)
        elif (callback_data.action == TaskEditAction.CHANGE_TIME_ZONE):
            message = task.reminder_date
            reply = create_time_zone_keyboard()
            await state.set_state(AlterTaskState.edit_time_zone)
        elif (callback_data.action == TaskEditAction.CHANGE_TIME):
            message = task.reminder_date.strftime('%H:%M')
            reply=create_time_picker_keyboard()
            await state.set_state(AlterTaskState.edit_time)

        await state.update_data(task_id=callback_data.id)
        await callback.message.answer(
            text=(message),
            reply_markup= reply
        )
    except Exception as error:
        logger.error(f'handle_task_edit: {error}')
        await callback.message.answer(error_message)


@router.message(AlterTaskState.edit_description, F.text)
async def handle_edit_description(
    message: Message,
    bot: Bot,
    state: FSMContext
) -> None:
    """
    Handles the task description edit.

    Args:
        message (Message): The incoming message object.
        bot (Bot): The bot instance.
        state (FSMContext): The state machine context.

    Returns:
        None
    """
    try:
        message.delete()
        task_id = (await state.get_data()).get('task_id')
        await db.edit_task_description(
            task_id=task_id,
            new_description=message.text
        )
        await state.clear()
        await bot.send_message(
            chat_id=message.from_user.id,
            text=(f'{msg_task_description_change_completed}\n\n{message.text}'),
            reply_markup=task_edit_kb(task_id)
        )
    except Exception as error:
        logger.error(f'handle_edit_description: {error}')
        await message.answer(error_message)
        await state.clear()


@router.message(AlterTaskState.edit_description)
async def handle_invalid_description_content_type(
    message: Message,
    bot: Bot
) -> None:
    """
    Handles the invalid content type for the task description.

    Args:
        message (Message): The incoming message object.
        bot (Bot): The bot instance.

    Returns:
        None
    """
    try:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=msg_task_createion_invalid_content_type,
            reply_markup=None
        )
    except Exception as error:
        logger.error(f'handle_invalid_description_content_type: {error}')


@router.callback_query(AlterTaskState.edit_date, SimpleCalendarCallback.filter())
async def handle_edit_date(
    callback: CallbackQuery,
    callback_data: dict,
    state: FSMContext
) -> None:
    """
    Handles the task date edit.

    Args:
        callback (CallbackQuery): The callback query instance.
        callback_data (dict): The callback data.
        state (FSMContext): The state machine context.
  
    Returns:
        None
    """
    try:
        await callback.answer()
        selected, date = await SimpleCalendar().process_selection(callback, callback_data)
        if selected:
            task_id = (await state.get_data()).get('task_id')
            task = await db.get_task_by_id(task_id)
            origianl_date = task.reminder_date
            replaced_date = origianl_date.replace(
                year=date.year,
                month=date.month,
                day=date.day
            )
            await db.update_task_reminder_date(
                task_id=task_id,
                reminder_date=replaced_date
            )
            await db.set_task_not_reminded(task_id=task_id)
            await state.clear()
            await callback.message.delete()
            await callback.message.answer(
                text=(f'{msg_task_date_change_completed}\n\n{replaced_date.strftime('%Y-%m-%d')}'),
                reply_markup=task_edit_kb(task_id)
            )

    except Exception as error:
        logger.error(f'handle_edit_date: {error}')
        await state.clear()