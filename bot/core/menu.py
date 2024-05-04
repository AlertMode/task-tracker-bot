from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Start the bot / Return to the main menu'
        ),

        BotCommand(
            command='createtask',
            description='Create a task'
        ),

        BotCommand(
            command='gettasks',
            description='Show all the lists with tasks'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())