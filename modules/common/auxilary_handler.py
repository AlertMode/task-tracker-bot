import re

from datetime import (
    datetime,
    time,
    timedelta,
    timezone
)

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from dateutil.relativedelta import relativedelta

from modules.set.recurring_reminder_callback import (
    DayOfWeek,
    ReminderInterval
)
from utils.logging_config import logger


MAX_REMINDER_INTERVAL = (365 * 5) + 1 


async def store_message_id(state: FSMContext, message_id: int) -> None:
    """
    Stores the message ID in the state.

    Args:
        state (FSMContext): The state of the conversation.
        message_id (int): The message ID.

    Returns:
        None
    """
    try:
        data = await state.get_data()
        messages = data.get('messages', [])
        messages.append(message_id)
        await state.update_data(messages=messages)
    except Exception as error:
        logger.error(f'store_message_id(): {error}')


async def get_stored_message_ids(state: FSMContext) -> list[int]:
    """
    Retrieves the stored message IDs from the state.

    Args:
        state (FSMContext): The state of the conversation.

    Returns:
        list[int]: The list of message IDs.
    """
    try:
        data = await state.get_data()
        return data.get('messages', [])
    except Exception as error:
        logger.error(f'Error: get_stored_message_ids(): {error}')
        return []


async def delete_all_messages(state: FSMContext, bot: Bot, chat_id: int) -> None:
    """
    Deletes all the messages in the conversation.

    Args:
        state (FSMContext): The state of the conversation.
        bot (Bot): The bot instance.
        chat_id (int): The chat ID.

    Returns:
        None
    """
    try:
        message_ids = await get_stored_message_ids(state=state)

        if not message_ids:
            return
        
        for message_id in message_ids:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
        
        await state.update_data(messages=[])
    except Exception as error:
        logger.error(f'delete_all_messages(): {error}')


def validate_time_format(input_time: str) -> time | None:
    """
    Validates the reminder time input.

    Args:
        input_time (str): The input time.

    Returns:
        time | None: The time object or None.
    """
    try:
        # Pattern to match HH:MM UTC+[number] with HH in 00-23 and MM in 00-59
        pattern = r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]) \+([+-]?[0-9]|1[0-4])$"
        match = re.match(pattern, input_time)
        if match:
            hours, minutes, utc_offset = map(int, match.groups())
            _timezone = timezone(timedelta(hours=utc_offset))
            return time(
                hour=hours,
                minute=minutes,
                tzinfo=_timezone
            )
        return None
    except Exception as error:
        logger.error(f'valid_reminder_time(): {error}')
        return None
    

def validate_interval_format(input_interval: str) -> int | None:
    """
    Validates the reminder interval input.

    Args:
        input_interval (str): The input interval.

    Returns:
        int | None: The interval or None.
    """
    try:
        global MAX_REMINDER_INTERVAL
        if input_interval.isdigit() and int(input_interval) > 0 and int(input_interval) < MAX_REMINDER_INTERVAL:
            return int(input_interval)
    except Exception as error:
        logger.error(f'validate_interval_format(): {error}')
        return None
    

def calculate_next_reminder_date(
        type: ReminderInterval,
        initial_datetime: datetime,
        interval: int,
        day_of_week: DayOfWeek = None
) -> datetime:
    """
    Calculates the next reminder time.

    Args:
        type (ReminderInterval): The type of the reminder interval.
        initial_datetime (datetime): The initial datetime.
        interval (int): The interval.

    Returns:
        datetime: The next reminder datetime.
    """
    try:
        result = None
        current_datetime_with_initial_time = datetime.now().replace(
            hour=initial_datetime.hour,
            minute=initial_datetime.minute,
            second=initial_datetime.second,
            microsecond=initial_datetime.microsecond,
            tzinfo=initial_datetime.tzinfo
        )

        current_weekday = current_datetime_with_initial_time.strftime('%A').upper()
        
        print(current_weekday)
        

        if type == ReminderInterval.BY_DAYS.value:
            result = current_datetime_with_initial_time + relativedelta(days=interval)
        elif type == ReminderInterval.BY_WEEKS.value:
            result = current_datetime_with_initial_time + relativedelta(weeks=interval)
        elif type == ReminderInterval.BY_MONTHS.value:
            result = current_datetime_with_initial_time + relativedelta(months=interval)
        elif type == ReminderInterval.BY_YEARS.value:
            result = current_datetime_with_initial_time + relativedelta(years=interval)
    except Exception as error:
        logger.error(f'calculate_next_reminder_date(): {error}')
    finally:
        return result


def convert_string_to_datetime(
        time_str: str,
        utc_offset_str: int
) -> datetime:
    """
    Converts the string to a datetime object.

    Args:
        time (str): The time string.
        utc_offset (int): The UTC offset.

    Returns:
        datetime: The datetime object.
    """
    try:
        time_obj = datetime.strptime(time_str, '%H:%M')
        sign = 1 if "+" in utc_offset_str else -1
        utc_offset_hours = int(utc_offset_str.replace("+", "").replace("-", ""))
        time_zone = timezone(timedelta(hours=sign * utc_offset_hours))

        return time_obj.replace(tzinfo=time_zone)
    except Exception as error:
        logger.error(f'convert_string_to_datetime(): {error}')
        return None