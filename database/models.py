import sqlite3
from database.connection import create_connection


def create_tables():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                users_id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                username TEXT NOT NULL,
                phone_number TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS diary_entries (
                entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                content TEXT NOT NULL,
                FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
            )''')

            conn.commit()
            print("Таблицы успешно созданы")
        except sqlite3.Error as e:
            print(f"Ошибка при создании таблиц: {e}")
        finally:
            conn.close()


def add_user(telegram_id, username, phone_number):
    conn = create_connection()
    if conn:
        try:
            sql = "INSERT INTO users (telegram_id, username, phone_number) VALUES (?, ?, ?)"
            cursor = conn.cursor()
            cursor.execute(sql, (telegram_id, username, phone_number))
            user_id = cursor.lastrowid
            conn.commit()
            print("Пользователь успешно добавлен")
            return user_id
        except sqlite3.Error as e:
            print((f"Произошла ошибка {e}"))
        finally:
            conn.close()

def add_diary_entry (telegram_id , content ):
    conn = create_connection()
    if conn:
        try:
            sql = "INSERT INTO diary_entries (telegram_id, content) VALUES (?, ?)"
            cursor = conn.cursor()
            cursor.execute(sql, (telegram_id , content))
            entry_id = cursor.lastrowid
            conn.commit()
            print("Запись успешно добавлена")
            return entry_id
        except sqlite3.Error as e:
            print(f"Произошла ошибка {e}")
        finally:
            conn.close()

def filter_diary_by_date(telegram_id, date):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Выполняем запрос с параметрами telegram_id и date
            cursor.execute("SELECT * FROM diary_entries WHERE telegram_id = ? AND date(date) = ?", (telegram_id, date))
            entries = cursor.fetchall()

            # Проверяем, есть ли записи
            if entries:
                print("\nВаши записи:")
                for entry in entries:
                    print(f"Дата: {entry[2]}, Запись: {entry[3]}")
            else:
                print("Записей за указанную дату не найдено.")

        except sqlite3.Error as e:
            print(f"Произошла ошибка {e}")
        finally:
            conn.close()


