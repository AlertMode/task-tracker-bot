from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from core.dictionary import *

return_to_main_menu_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=MainMenuReplyKeyboard.MAIN_MENU)
    ]
], resize_keyboard=True, one_time_keyboard=True)