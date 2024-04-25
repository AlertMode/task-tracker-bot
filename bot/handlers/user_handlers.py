import sqlite3

from aiogram.filters import Command
from aiogram import Router, types

from database.database import create_list_table, create_task_table, create_list, create_task, create_default_list

user_router = Router()


# Initialize the database
connection = sqlite3.connect("tasks.db")
create_list_table(connection)
create_task_table(connection)
create_default_list(connection)

@user_router.message(Command('start'))
async def cmd_start(msg: types.Message) -> None:
    """Processes the `start` command"""
    await msg.answer(
        """
            Hi there\! I\'m *TaskTracker* \- a Telegram bot for efficient task management\.
        """
    )

@user_router.message(Command("newlist"))
async def cmd_new_list(msg: types.Message) -> None:
    """Process the `newlist` command"""
    try:
        list_name = msg.text.split("/newlist", 1)[1]
        create_list(connection, list_name)
        await msg.answer(f"List '{list_name}' has been created\!")
    except IndexError:
        await msg.answer("Please, provide a list name after `addlist`")

#TODO
# @user_router.message(Command("addtask"))
# async def cmd_add_task(msg: types.Message) -> None:
#     """Processes the `addtask` command"""
#     try:
#         task_description = msg.text.split("/addtask", 1)[1]
#         create_task(connection, task_description)
#         await msg.answer(f"Task '{task_description}' has been added!")
#     except IndexError:
#         await msg.answer("Please, provide a task description after `add_task`")
        