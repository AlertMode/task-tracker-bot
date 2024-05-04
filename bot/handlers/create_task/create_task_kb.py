from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


cancel_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='cancel')
    ]
], resize_keyboard=True, one_time_keyboard=True)