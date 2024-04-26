from aiogram import Bot
from aiogram.enums import ParseMode

from token_api import TOKEN_API

bot = Bot(
    token=TOKEN_API,
    parse_mode=ParseMode.HTML
)