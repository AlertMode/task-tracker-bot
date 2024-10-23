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

from utils.logging_config import logger
    

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