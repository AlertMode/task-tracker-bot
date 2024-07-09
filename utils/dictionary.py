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
button_common_confirm = '🆗'
button_common_skip = '⏭️ Skip'


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
task_reminder_no_days_selected = '🚧 No days were selected'
task_reminder_time = '🔔 Set the reminder time'

button_task_reminder_unchecked = '🔲 %s'
button_task_reminder_checked = '✅ %s'
button_task_reminder_recurring = '🔁 Recurring'
button_task_reminder_single = '⏰ Single'


#Reminder Interval
task_reminder_interval_message = '📅 Choose the interval'

button_task_reminder_daily = '📅 Daily'
button_task_reminder_weekly = '📅 Weekly'
button_task_reminder_monthly = '📅 Monthly'
button_task_reminder_yearly = '📅 Yearly'

#Single reminder
single_reminder_message = '📅 Set the reminder date'


#Task management
task_status_message = '📁 Task status:'

ongoing_tasks = '▶️ Ongoing'
completed_tasks = '⏹️ Completed'

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