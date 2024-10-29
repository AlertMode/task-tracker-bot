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
    

def convert_string_to_timezone(
        utc_str: str
) -> timezone:
    """
    Converts the string to a timezone.

    Args:
        utc_str (str): The time string.

    Returns:
        int: The timezone.
    """
    try:
        # Extract the sign and the hours from the UTC offset
        sign = 1 if "+" in utc_str else -1

        # Extract the hours from the UTC offset
        utc_offset_hours = int(utc_str.replace("+", "").replace("-", ""))

        return timezone(timedelta(hours=sign * utc_offset_hours))
    except Exception as error:
        logger.error(f'convert_string_to_timezone(): {error}')
        return None


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
        time_zone = convert_string_to_timezone(utc_offset_str)
        return time_obj.replace(tzinfo=time_zone)
    except Exception as error:
        logger.error(f'convert_string_to_datetime(): {error}')
        return None