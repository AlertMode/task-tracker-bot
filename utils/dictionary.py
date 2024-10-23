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
msg_date_selection = '📅 Choose the date'
mag_task_creation_cancel_cmd = '❌ Task creation has been cancelled'
msg_task_creation_completed = '☑️ Task saved: <b>%s</b>'
msg_task_createion_invalid_content_type = '❓ Please, type in a text'
msg_final_confirmation = (
    '📜 Task: <b>%s</b>\n'
    '📅 Date: <b>%s</b>'
)


#Reminder setting
task_reminder_timezone = '🌐 Set the timezone'
task_reminder_time_picker = '🕒 Set the reminder time'
single_reminder_message = '📅 Set the reminder date'


#Task management
task_status_message = '📁 Task status:'

ongoing_tasks = '▶️ Ongoing'
completed_tasks = '⏹️ Completed'

task_ongoing = (
    '📅 <b>Createion date:</b> %s\n'
    '📜 <b>Description:</b> %s\n'
    '▶️ <b>Reminder date:</b> %s\n'
)
task_completed = (
    '📅 <b>Createion date:</b> %s\n'
    '📜 <b>Description:</b> %s\n'
    '✅ <b>Completion date:</b> %s\n'
)
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