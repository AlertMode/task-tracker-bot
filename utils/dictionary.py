start_message = (
    f'<b>TaskTracker</b> - a task management bot.'
)


#Error
error_message = '⚠️ Something went wrong! Please, try again'


#Common buttons
btn_common_forward = '➡️'
btn_common_backwards = '⬅️'
btn_common_return = '🔙'
btn_common_number_one = '1️⃣'
btn_common_confirm = '🆗'
btn_common_cancel = '🚫'
btn_common_skip = '⏭️ Skip'


#Reply main menu commands
class MenuNames:
    GET_TASKS = '🗃️ Show tasks'
    NEW_TASK = '✒️ New task'
    MAIN_MENU = '↩️ Main Menu'


#Task creation
msg_task_creation_description_prompt = '✍ Input the task:'
mag_task_creation_cancel_cmd = '❌ Task creation has been cancelled'
msg_task_creation_completed = '☑️ Task saved: <b>%s</b>'
msg_task_createion_invalid_content_type = '❓ Please, type in a text'
msg_reminder_final_confirmation = (
    '📅 Task: <b>%s</b>\n\n'
    '⏰ Time: <b>%s</b>\n\n'
    '🔁 Interval: Each <b>%s</b> <b>%s</b>\n\n\n'
)

#Reminder setting
task_reminder_type_selection = '🔔 Choose the reminder type'
task_reminder_message = '📅 Choose the day'
task_reminder_no_days_selected = '🚧 No days were selected'
task_reminder_time = ('🕒 Set the reminder time in the format ' 
                     '<b>HH:MM +UTC</b> (e.g., 12:34 +3)')
task_remimder_invalid_time_format = '❓ Invalid time format! Please, try again!'
task_reminder_interval_selection = '📅 Choose the interval: daily interval or weekly interval or etc'
msg_reminder_invalid_interval_number = (
    '❓ Invalid interval format!\n'
    'Please, type in an integer value!'
)

button_task_reminder_unchecked = '🔲 %s'
button_task_reminder_checked = '✅ %s'
button_task_reminder_recurring = '🔁 Recurring'
button_task_reminder_single = '⏰ Single'


#Reminder Interval
task_reminder_interval_selection = '⏱ Choose the interval: daily interval or weekly interval or etc'
msg_reminder_interval_number = '⏱ Set the interval number. Only integer values!'

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