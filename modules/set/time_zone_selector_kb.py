from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.set.time_zone_selector_callback import *
from utils.logging_config import logger

def create_time_zone_keyboard() -> InlineKeyboardButton:
    """
    Creates an inline keyboard for selecting a time zone using the TimeZone enum.
    
    Returns:
        InlineKeyboardMarkup: Inline keyboard with UTC time zones.
    """
    try:
        builder = InlineKeyboardBuilder()

        # Loop through the TimeZone enum to create buttons for each time zone
        for time_zone in TimeZone:
            builder.button(
                text=f"UTC{time_zone.value}",
                callback_data=TimeZoneSelectorCallbackData(time_zone=time_zone).pack()
            )
        
        builder.adjust(5)
        
        return builder.as_markup()
    except Exception as error:
        logger.error(f"create_time_zone_keyboard: {error}")
        return None