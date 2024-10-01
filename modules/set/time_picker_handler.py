from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from modules.add.task_creation_kb import final_confirmation_kb
from modules.add.task_creation_state import CreateState
from modules.common.auxilary_handler import *
from modules.set.time_picker_callback import *
from modules.set.time_picker_kb import create_time_picker_keyboard
from utils.dictionary import *
from utils.logging_config import logger


router = Router(name=__name__)


@router.callback_query(CreateState.reimnder_time_picker)
async def handle_time_picker_selector(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    try:
        # Log the received callback data for debugging
        logger.info(f"Received callback data: {callback.data}")

        # Extract callback data
        callback_data = TimePickerCallbackData.unpack(callback.data)

        # Check if the action is 'CONFIRM'
        if callback_data.action == TimePickerAction.CONFIRM:
            data = await state.get_data()

            selected_time = f"{callback_data.hours_tens}{callback_data.hours_ones}:{callback_data.minutes_tens}{callback_data.minutes_ones}"
            
            # Log the final selected time for debugging
            logger.info(f"Final selected time: {selected_time}")

            # Update the state with the final time
            await state.update_data(reminder_time=selected_time)


            #TODO: Fix the issue with the reminder time
            #TODO: Write the code for calling timezone picker
            description_task = data.get("description_task")
            single_date = data.get("single_date")
            reminder_time = data.get("reminder_time")

            await state.set_state(CreateState.final_confirmation)
            await callback.answer(f"Time confirmed: {selected_time}")
            await callback.message.answer(
                text=msg_task_single_reminder_final_confirmation % (
                    description_task,
                    single_date,
                    reminder_time
                ),
                reply_markup=final_confirmation_kb()
            )
            return
        
        default_hour_tens = HoursTens.ZERO.value
        default_hour_ones = HoursOnes.ZERO.value
        default_minute_tens = MinutesTens.ZERO.value
        default_minute_ones = MinutesOnes.ZERO.value

        # Retrieve current time from the state or set to defaults if missing
        data = await state.get_data()
        current_hours_tens = data.get("hours_tens", default_hour_tens)
        current_hours_ones = data.get("hours_ones", default_hour_ones)
        current_minutes_tens = data.get("minutes_tens", default_minute_tens)
        current_minutes_ones = data.get("minutes_ones", default_minute_ones)

        # Use callback data to update the current time
        hours_tens = callback_data.hours_tens or current_hours_tens
        hours_ones = callback_data.hours_ones or current_hours_ones
        minutes_tens = callback_data.minutes_tens or current_minutes_tens
        minutes_ones = callback_data.minutes_ones or current_minutes_ones

        # Check if the time has actually changed
        if (hours_tens == current_hours_tens and hours_ones == current_hours_ones and
            minutes_tens == current_minutes_tens and minutes_ones == current_minutes_ones):
            await callback.answer("No changes were made to the time.")
            return

        # Update state with the new time
        await state.update_data(
            hours_tens=hours_tens,
            hours_ones=hours_ones,
            minutes_tens=minutes_tens,
            minutes_ones=minutes_ones
        )

        # Regenerate the time picker keyboard with the updated time
        keyboard = create_time_picker_keyboard(hours_tens, hours_ones, minutes_tens, minutes_ones)

        # Edit the message to reflect the new time selection
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        
        await callback.answer()

    except Exception as error:
        logger.error(f"handle_time_picker_selector: {error}")
        await callback.answer("An error occurred while selecting the time. Please try again.")