import os
from aiogram import Bot
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = Bot(
    token=TOKEN,
    parse_mode=ParseMode.HTML
)