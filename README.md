# task-tracker-bot
### Video Demo: https://youtu.be/B6R1lQd_w4s?si=fslZLdyQBy-biKhn
### Description:
Task Tracker Bot is a Telegram-based task management application designed to simplify creating, managing, and receiving reminders for tasks directly through Telegram. This bot leverages Aiogram for interaction handling and SQLAlchemy with an asynchronous MySQL database for data persistence, ensuring a responsive and efficient experience. The bot is ideal for users who prefer task management on-the-go without needing additional apps, offering simple task creation, modification, and notifications within a familiar messaging platform.

Task Tracker Bot supports user-friendly task creation and editing with time zone-based reminders, making it ideal for users across various regions. Reminders are personalized to each user’s local time zone, so notifications arrive accurately based on each user's location.

## Features

### 1. Task Creation and Management
- Users can add tasks with a description and specific deadline, directly storing these details in the database. Each task is associated with a unique user ID, enabling users to manage their tasks independently within the bot. The bot uses an intuitive process for adding and editing tasks, ensuring that all entries are accessible and manageable.

### 2. Flexible Reminder Scheduling
- Reminders are customizable to each user’s needs. With support for different time zones, the bot schedules reminders to align accurately with each user’s local time, reducing confusion around scheduling.

### 3. Automated Notifications
- A background scheduler periodically checks for upcoming tasks and sends reminders for tasks nearing their due time. Notifications arrive as Telegram messages, with options for users to mark tasks as complete or snooze reminders if needed.

### 4. Interactive Bot Controls
- Users can interact with the bot to mark tasks as complete, edit details or delete tasks directly from reminder messages.

### 5. Data Persistence
- All task and reminder data are stored in a MySQL database, ensuring user information is retained between sessions and restarts. The asynchronous MySQL setup helps handle large numbers of users and tasks, providing reliable storage and fast retrieval times even as the user base grows.

### 6. Logging and Error Handling
- The bot includes logging functionality to track user interactions and errors, ensuring a robust and reliable experience. If any error occurs, it is logged for further inspection, making troubleshooting simpler for developers and contributing to a smoother user experience.

## Persistenceroject Structure Overview
### database/:
- __database.py__ Manages the connection to the MySQL database and defines core methods for interacting with the database,
such as adding, updating, retreving and deleting tasks.
- __models.py__ Defines the data models (tables) for the database, including structures for users and tasks.
### modules/:
- __add/, alter/, list/, set/, start/:__  Contain handlers or modules that correspond to specific bot functionalities like adding tasks, altering existing tasks, listing tasks, setting reminders, and starting interactions with users.
- __common/:__ Houses shared utilities that are used across multiple modules.
### routers/:
- __routers.py:__ Defines how different commands or message types are routed to specific handlers, organizing how user interactions are processed.
### utils/:
- __dictionary.py:__ Provides a dictionary or helper phrases and responses for the bot.
- **logging_config.py:** Manages logging configurations, helping with debugging and tracking issues during runtime.
### bot_instance.py:
- Initializes and configures the bot instance using the token from .env. It’s the central setup for connecting the bot to Telegram.
### .env:
- Stores environment variables like the bot token and database credentials.
### bot_instance.py:
- Initializes and configures the bot instance using the token from .env.
### main.py:
- Initializes the bot and starts polling for user messages, acting as the launcher for the application.

### menu.py:
- Defines the main menu structure that users interact with within the bot.
### scheduler_handler.py:
- Manages scheduled tasks, such as periodic checks for due reminders and sending notifications to users.
## Installation and Usage

### 1. Clone this repository
```
git clone https://github.com/AlertMode/task-tracker-bot
cd task-tracker-bot
```

### 2. Install Dependecies
This bot requires Python 3.9 or above. Install the necessary dependencies with!
```
pip install -r requirements.txt
```

### 3. Setup your Telegram bot token.

### 4. Setup MySQL Database:
Configure your MySQL database and update the database URI in **database.py** accordingly.

### 5. Configure .env file in the root folder of the project:
```
TOKEN = <Your Telegram Bot Token>
ADMIN_ID = <Admin's Telegram ID>

DB_NAME = <Your Database Name>
DB_USER = <Your Database User>
DB_PASSWORD = <Your Database Password>
DB_HOST = '127.0.0.1'
```

## Contributing

Contributions are welcome! Feel free to enhance TaskTracker Bot's functionality, improve documentation, or fix any issues.
