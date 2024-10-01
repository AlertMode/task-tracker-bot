from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.common.actions_callback import *
from modules.set.time_picker_callback import *
from utils.dictionary import *
from utils.logging_config import logger


from typing import Tuple

def increment_hours_tens(current_value: str, hours_ones: str) -> Tuple[str, str]:
    """
    Increment the hours' tens value (0-2). If the new tens value is '2' and ones is greater than '3', set ones to '0'.

    Args:
        current_value (str): The current value of hours' tens.
        hours_ones (str): The current value of hours' ones.

    Returns:
        (str, str): The incremented value of hours' tens and the adjusted ones if necessary.
    """
    new_tens = str((int(current_value) + 1) % 3)
    # If tens become '2', ensure ones does not exceed '3'
    new_ones = '0' if new_tens == '2' and int(hours_ones) > 3 else hours_ones
    return new_tens, new_ones


def decrement_hours_tens(current_value: str, hours_ones: str) -> Tuple[str, str]:
    """
    Decrement the hours' tens value (0-2). If the new tens value is '2' and ones is greater than '3', set ones to '0'.

    Args:
        current_value (str): The current value of hours' tens.
        hours_ones (str): The current value of hours' ones.

    Returns:
        (str, str): The decremented value of hours' tens and the adjusted ones if necessary.
    """
    new_tens = str((int(current_value) - 1) % 3)
    # If tens become '2', ensure ones does not exceed '3'
    new_ones = '0' if new_tens == '2' and int(hours_ones) > 3 else hours_ones
    return new_tens, new_ones



def increment_hours_ones(current_value: str, hours_tens: str) -> str:
    """
    Increment the hours' ones value (0-9). If hours_tens is '2', limit ones to 0-3.

    Args:
        current_value (str): The current value of hours' ones.
        hours_tens (str): The current value of hours' tens.

    Returns:
        str: The incremented value of hours' ones with range constraint.
    """
    max_ones = 3 if hours_tens == '2' else 9
    return str((int(current_value) + 1) % (max_ones + 1))


def decrement_hours_ones(current_value: str, hours_tens: str) -> str:
    """
    Decrement the hours' ones value (0-9). If hours_tens is '2', limit ones to 0-3.

    Args:
        current_value (str): The current value of hours' ones.
        hours_tens (str): The current value of hours' tens.

    Returns:
        str: The decremented value of hours' ones with range constraint.
    """
    max_ones = 3 if hours_tens == '2' else 9
    return str((int(current_value) - 1) % (max_ones + 1))


def increment_minutes_tens(current_value: str) -> str:
    """
    Increment the minutes' tens value (0-5).

    Args:
        current_value (str): The current value of minutes' tens.

    Returns:
        str: The incremented value of minutes' tens.
    """
    return str((int(current_value) + 1) % 6)


def decrement_minutes_tens(current_value: str) -> str:
    """
    Decrement the minutes' tens value (0-5).

    Args:
        current_value (str): The current value of minutes' tens.

    Returns:
        str: The decremented value of minutes' tens.
    """
    return str((int(current_value) - 1) % 6)


def increment_minutes_ones(current_value: str) -> str:
    """
    Increment the minutes' ones value (0-9).

    Args:
        current_value (str): The current value of minutes' ones.

    Returns:
        str: The incremented value of minutes' ones.
    """
    return str((int(current_value) + 1) % 10)


def decrement_minutes_ones(current_value: str) -> str:
    """
    Decrement the minutes' ones value (0-9).

    Args:
        current_value (str): The current value of minutes' ones.

    Returns:
        str: The decremented value of minutes' ones.
    """
    return str((int(current_value) - 1) % 10)


def create_increment_decrement_buttons(
    hours_tens: HoursTens,
    hours_ones: HoursOnes,
    minutes_tens: MinutesTens,
    minutes_ones: MinutesOnes
) -> list:
    """
    Creates the increment and decrement button rows for hours and minutes.

    Args:
        hours_tens (HoursTens): The tens digit of the hour.
        hours_ones (HoursOnes): The ones digit of the hour.
        minutes_tens (MinutesTens): The tens digit of the minute.
        minutes_ones (MinutesOnes): The ones digit of the minute.

    Returns:
        list: A list of InlineKeyboardButtons representing both increment and decrement rows.
    """
    try:
        # Increment hours tens, check if hours ones needs to be reset
        new_hours_tens, new_hours_ones = increment_hours_tens(hours_tens, hours_ones)
        increment_buttons = [
            InlineKeyboardButton(
                text='🔼',
                callback_data=TimePickerCallbackData(
                    hours_tens=new_hours_tens,
                    hours_ones=new_hours_ones,
                    minutes_tens=minutes_tens,
                    minutes_ones=minutes_ones
                ).pack()
            ),
            InlineKeyboardButton(
                text='🔼',
                callback_data=TimePickerCallbackData(
                    hours_tens=hours_tens,
                    hours_ones=increment_hours_ones(hours_ones, hours_tens),
                    minutes_tens=minutes_tens,
                    minutes_ones=minutes_ones
                ).pack()
            ),
            InlineKeyboardButton(
                text='🔼',
                callback_data=TimePickerCallbackData(
                    hours_tens=hours_tens,
                    hours_ones=hours_ones,
                    minutes_tens=increment_minutes_tens(minutes_tens),
                    minutes_ones=minutes_ones
                ).pack()
            ),
            InlineKeyboardButton(
                text='🔼',
                callback_data=TimePickerCallbackData(
                    hours_tens=hours_tens,
                    hours_ones=hours_ones,
                    minutes_tens=minutes_tens,
                    minutes_ones=increment_minutes_ones(minutes_ones)
                ).pack()
            )
        ]

        # Decrement hours tens, check if hours ones needs to be reset
        new_hours_tens, new_hours_ones = decrement_hours_tens(hours_tens, hours_ones)
        decrement_buttons = [
            InlineKeyboardButton(
                text='🔽',
                callback_data=TimePickerCallbackData(
                    hours_tens=new_hours_tens,
                    hours_ones=new_hours_ones,
                    minutes_tens=minutes_tens,
                    minutes_ones=minutes_ones
                ).pack()
            ),
            InlineKeyboardButton(
                text='🔽',
                callback_data=TimePickerCallbackData(
                    hours_tens=hours_tens,
                    hours_ones=decrement_hours_ones(hours_ones, hours_tens),
                    minutes_tens=minutes_tens,
                    minutes_ones=minutes_ones
                ).pack()
            ),
            InlineKeyboardButton(
                text='🔽',
                callback_data=TimePickerCallbackData(
                    hours_tens=hours_tens,
                    hours_ones=hours_ones,
                    minutes_tens=decrement_minutes_tens(minutes_tens),
                    minutes_ones=minutes_ones
                ).pack()
            ),
            InlineKeyboardButton(
                text='🔽',
                callback_data=TimePickerCallbackData(
                    hours_tens=hours_tens,
                    hours_ones=hours_ones,
                    minutes_tens=minutes_tens,
                    minutes_ones=decrement_minutes_ones(minutes_ones)
                ).pack()
            )
        ]

        return [increment_buttons, decrement_buttons]
    except Exception as error:
        logger.error(f"create_increment_decrement_buttons: {error}")


def create_display_row(
        hours_tens: HoursTens,
        hours_ones: HoursOnes,
        minutes_tens: MinutesTens,
        minutes_ones: MinutesOnes
    ) -> list:
    """
    Creates the display row for the current time values (hours and minutes).

    Args:
        hours_tens (HoursTens): The tens digit of the hour.
        hours_ones (HoursOnes): The ones digit of the hour.
        minutes_tens (MinutesTens): The tens digit of the minute.
        minutes_ones (MinutesOnes): The ones digit of the minute.

    Returns:
        list: A list of InlineKeyboardButtons displaying the current time values.
    """
    try:
        return [
            InlineKeyboardButton(text=f'{hours_tens}', callback_data='noop'),
            InlineKeyboardButton(text=f'{hours_ones}', callback_data='noop'),
            InlineKeyboardButton(text=f'{minutes_tens}', callback_data='noop'),
            InlineKeyboardButton(text=f'{minutes_ones}', callback_data='noop')
        ]
    except Exception as error:
        logger.error(f"create_display_row: {error}")


def create_confirm_button(
        hours_tens: HoursTens,
        hours_ones: HoursOnes,
        minutes_tens: MinutesTens,
        minutes_ones: MinutesOnes
    ) -> InlineKeyboardButton:
    """
    Creates the confirm button that sends the selected time.

    Args:
        hours_tens (HoursTens): The tens digit of the hour.
        hours_ones (HoursOnes): The ones digit of the hour.
        minutes_tens (MinutesTens): The tens digit of the minute.
        minutes_ones (MinutesOnes): The ones digit of the minute.

    Returns:
        InlineKeyboardButton: The button to confirm the selected time.
    """
    try:
        return InlineKeyboardButton(
            text='CONFIRM',
            callback_data=TimePickerCallbackData(
                hours_tens=hours_tens,
                hours_ones=hours_ones,
                minutes_tens=minutes_tens,
                minutes_ones=minutes_ones,
                action=TimePickerAction.CONFIRM
            ).pack()
        )
    except Exception as error:
        logger.error(f"create_confirm_button: {error}")


def create_time_picker_keyboard(
        hours_tens: HoursTens = HoursTens.ZERO,
        hours_ones: HoursOnes = HoursOnes.ZERO,
        minutes_tens: MinutesTens = MinutesTens.ZERO,
        minutes_ones: MinutesOnes = MinutesOnes.ZERO
    ) -> InlineKeyboardMarkup:
    """
    Creates a compact inline keyboard for selecting time.

    Args:
        hours_tens (HoursTens): The tens digit of the hour.
        hours_ones (HoursOnes): The ones digit of the hour.
        minutes_tens (MinutesTens): The tens digit of the minute.
        minutes_ones (MinutesOnes): The ones digit of the minute.

    Returns:
        InlineKeyboardMarkup: The inline keyboard for time picking.
    """
    try:
        builder = InlineKeyboardBuilder()

        # Add increment row
        increment_buttons, decrement_buttons = create_increment_decrement_buttons(
            hours_tens, hours_ones, minutes_tens, minutes_ones
        )
        builder.row(*increment_buttons)

        # Add the current time display row
        builder.row(*create_display_row(hours_tens, hours_ones, minutes_tens, minutes_ones))

        # Add decrement row
        builder.row(*decrement_buttons)

        # Add confirm button
        builder.row(create_confirm_button(hours_tens, hours_ones, minutes_tens, minutes_ones))

        return builder.as_markup()
    except Exception as error:
        logger.error(f"create_time_picker_keyboard: {error}")
