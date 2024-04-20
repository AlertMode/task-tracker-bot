# task-tracker-bot
### Video Demo: <URL HERE>
### Description:
TaskTracker Bot: A Telegram bot for efficient task management. Add, list, mark, and remove tasks with ease. Set reminders and manage custom lists.

## Features
* **Start:** 
    * ```/start``` - Get started with the bot.

* **Add Tasks:**
    * ```/add [task]``` - Add a new task to your default list.
    * ```/add [list name] [task]``` - Add a task to a specific list (e.g., /add groceries buy milk).

* **List Tasks:**
    * ```/list``` - View all tasks in your default list.
    * ```/list [list name]``` - View all tasks in a specific list.

* **Mark Tasks Complete:**
    * ```/done [task number]``` - Mark a task as completed in your default list.
    * ```/done [list name] [task number]``` - Mark a task as completed in a specific list.

* **Remove Tasks:**
    * ```/remove [task number]``` - Remove a task from your default list.
    * ```/remove [list name] [task number]``` - Remove a task from a specific list.

* **Get Help:**
    * ```/help``` - See a list of all available commands and their functionalities.

* **Show Lists:**
  * ```/showlists``` - View all your created lists.

* **Manage Lists:**
    * ```/newlist [list name]``` - Create a new list.
    * ```/deletelist [list name]``` - Delete a specific list (including its tasks).

* **Clear Tasks:**
    * ```/clear [list name]``` - Clear all tasks from a specific list. If no list is provided, it clears your default list.

* **Set Reminders:**
    * ```/remind [task number] [time] [repeat (optional)]``` - Set a one-time or recurring reminder for a task. [time] format will be specified later.
    * ```/remind [list name] [task number] [time] [repeat (optional)]``` - Similar to above, but for a specific list.

* **Make Tasks Repeatable:**
    * ```/repeat [task number] [interval]``` - Make a specific task repeat at a set interval which will be specified a bit later.
    * ```/repeat [list name] [task number] [interval]``` - Similar to above, but for a specific list.

## Installation and Usage

1. Clone this repository.
2. Set up your Telegram bot token.
3. Deploy the bot using your preferred hosting service.
4. Start managing your tasks with TaskTracker Bot!

## Contributing

Contributions are welcome! Feel free to enhance TaskTracker Bot's functionality, improve documentation, or fix any issues.
