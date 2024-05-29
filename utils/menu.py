from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

from utils.dictionary import MenuCommands


async def set_menu(bot: Bot):
    commands = [
        BotCommand(
            command=MenuCommands.START,
            description='Start the bot / Return to the main menu'
        ),

        BotCommand(
            command=MenuCommands.CREATE_TASK,
            description='Create a task'
        ),

        BotCommand(
            command=MenuCommands.GET_TASKS,
            description='Show tasks'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())