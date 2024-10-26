import sqlite3
from .connection import create_connection


def create_tables():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                phone_number TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS diary_entries (
                entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                content TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )''')

            conn.commit()
            print("Таблицы успешно созданы")
        except sqlite3.Error as e:
            print(f"Ошибка при создании таблиц: {e}")
        finally:
            conn.close()
