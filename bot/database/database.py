import sqlite3
from datetime import datetime

def create_list_table(connection):
    cursor = connection.cursor()
    cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_of_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
            date_of_completeion DATETIME
        )
    """
    )
    connection.commit()

def create_task_table(connection):
    cursor = connection.cursor()
    cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            list_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            date_of_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
            date_of_completion DATETIME,
            FOREIGN KEY(list_id) REFERENCES lists(id)
        )
    """
    )
    connection.commit()

def create_default_list(connection):
    cursor = connection.cursor()
    cursor.execute(
    """
        INSERT INTO lists (name)
        SELECT 'default'
        WHERE NOT EXISTS (
            SELECT 1 FROM lists WHERE name = 'default'
        );
    """
    )

def create_list(connection, name):
    cursor = connection.cursor()
    cursor.execute(
        """
            INSERT INTO lists (name) VALUES (?)
        """
        , (name,)
    )
    connection.commit()

def create_task(connection, list_id, description):
    cursor = connection.cursor()
    cursor.execute(
        """
            INSERT INTO tasks (list_id, description) VALUES (?)
        """
        , (list_id, description)
    )
    connection.commit()