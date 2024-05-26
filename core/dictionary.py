# Greeting message
from enum import Enum


start_message = (
    f'Hi!'
    'I\'m <b>TaskTracker</b> - a Telegram bot for efficient task management!'
)


#Error
error_message = '⚠️ Something went wrong! Please, try again'


#Menu commands
class MenuCommands(Enum):
    START = '/start'
    CREATE_TASK = '/create_task'
    GET_TASKS = '/get_tasks'


#Reply main menu commands
class MenuNames:
    GET_TASKS = '🗃️ Show tasks'
    NEW_TASK = '✒️ New task'
    MAIN_MENU = '↩️ Main Menu'


#Task creation
task_creation_description_prompt = '✍ Write your task\'s description'
task_creation_cancel_cmd = '❌ Task creation has been cancelled'
task_creation_completed = '☑️ Task has been created'
task_createion_invalid_content_type = '❓ Please, type in a text'



#Task management
task_status_message = '📁 Task status:'

task_ongoing = '▶️  %s \n\n <b>%s</b> \n\n➡️  %s'
task_completed = '▶️  %s \n\n <b><s>%s</s></b> \n\n✅  %s'
task_void_message = '🚧 No tasks were found! 🚧'

button_task_done = '✅ Done'
button_task_undone = '🔁 Restore'
button_task_edit = '✏️ Edit'
button_task_delete = '🗑️ Delete'

task_setting_done_completed = (f'Congratulations! 🎉\n\n'
                               'Task has been done!')
task_deletion_completed = '🚮 Task has been deleted'

task_setting_undone_completed = (f'Task has been restored\n\n'
                                 'Good luck! 😉')