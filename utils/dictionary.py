start_message = (
    f'<b>TaskTracker</b> - a task management bot.'
)


#Error
error_message = '⚠️ Something went wrong! Please, try again'


#Common buttons
button_common_forward = '➡️'
button_common_backwards = '⬅️'
button_common_return = '🔙'
button_common_number_one = '1️⃣'


#Reply main menu commands
class MenuNames:
    GET_TASKS = '🗃️ Show tasks'
    NEW_TASK = '✒️ New task'
    MAIN_MENU = '↩️ Main Menu'


#Task creation
task_creation_description_prompt = '✍ Input the task:'
task_creation_cancel_cmd = '❌ Task creation has been cancelled'
task_creation_completed = '☑️ Task saved: <b>%s</b>'
task_createion_invalid_content_type = '❓ Please, type in a text'


#Reminder setting
task_reminder_type_selection = '🔔 Choose the reminder type'
task_reminder_message = '📅 Choose the day'

button_task_reminder_unchecked = '🔲 %s'
button_task_reminder_checked = '✅ %s'
button_task_reminder_confirm = '🆗'
button_task_reminder_skip = '⏭️ Skip'
button_task_reminder_recurring = '🔁 Recurring'
button_task_reminder_single = '⏰ Single'


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