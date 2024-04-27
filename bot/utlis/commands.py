from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Start the bot'
        ),
        BotCommand(
            command='help',
            description='Informtaion about the bot\'s functionality'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())