msg_start_message = (
    f'<b>TaskTracker</b> - a task management bot.'
)


#Error
msg_error = '⚠️ Something went wrong! Please, try again'


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
    EDIT_MENU = '📝 Edit task'


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
msg_task_reminder_timezone = '🌐 Set the timezone'
msg_task_reminder_time_picker = '🕒 Set the reminder time'
msg_task_reminder_date = '📅 Set the reminder date'


#Task management
msg_task_status = '📁 Task status:'

msg_ongoing_tasks = '▶️ Ongoing'
msg_completed_tasks = '⏹️ Completed'

msg_task_ongoing = (
    '📅 <b>Creation date:</b> %s\n'
    '📜 <b>Description:</b> %s\n'
    '▶️ <b>Reminder date:</b> %s\n'
)
msg_task_completed = (
    '📅 <b>Creation date:</b> %s\n'
    '📜 <b>Description:</b> %s\n'
    '✅ <b>Completion date:</b> %s\n'
)
msg_task_void = '🚧 No tasks were found! 🚧'

btn_task_done = '✅ Done'
btn_task_undone = '🔁 Restore'
btn_task_edit = '✏️ Edit'
btn_task_delete = '🗑️ Delete'

msg_task_setting_done_completed = (f'Congratulations! 🎉\n\n'
                               'Task has been done!')
msg_task_deletion_completed = '🚮 Task has been deleted'

msg_task_setting_undone_completed = (f'Task has been restored\n\n'
                                 'Good luck! 😉')

btn_task_edit_description = '✏️ Edit description'
btn_task_edit_time = '🕒 Edit time'
btn_task_edit_timezone = '🌐 Edit timezone'
btn_task_edit_date = '📅 Edit date'

msg_edit_task = '📝 Chose the edit option:'

msg_task_description_change_completed = '✅ Description has been changed'
msg_task_date_change_completed = '✅ Date has been changed'
msg_task_time_change_completed = '✅ Time has been changed'
msg_task_timezone_change_completed = '✅ Timezone has been changed'

msg_edit_task_description_cancel = '❌ Editing the description has been cancelled'