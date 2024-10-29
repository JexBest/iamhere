import sqlite3
from database.connection import create_connection
from datetime import datetime

from database.see_all_content import cursor


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


# Создание таблицы аудита
def create_audit_table():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_log (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER,
                    phone_number TEXT,
                    action TEXT,
                    action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_created_at TIMESTAMP,
                    entry_created_at TIMESTAMP,
                    old_content TEXT,
                    new_content TEXT
                )
            ''')
            conn.commit()
            print("Таблица аудита успешно создана.")
        except sqlite3.Error as e:
            print(f"Ошибка при создании таблицы аудита: {e}")
        finally:
            conn.close()

# Функция для добавления записи в лог
def add_audit_log(telegram_id, phone_number, action, user_created_at=None, entry_created_at=None, old_content=None, new_content=None):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = '''
                INSERT INTO audit_log (telegram_id, phone_number, action, user_created_at, entry_created_at, old_content, new_content)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(sql, (telegram_id, phone_number, action, user_created_at, entry_created_at, old_content, new_content))
            conn.commit()
            print("Запись добавлена в журнал аудита.")
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении записи в журнал аудита: {e}")
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
            add_audit_log(
                telegram_id=telegram_id,
                entry_created_at=username,
                phone_number=phone_number,
                action="create_user",
                user_created_at=datetime.now()  # можно также запросить из таблицы, если нужно точное значение
            )
            return user_id
        except sqlite3.Error as e:
            print((f"Произошла ошибка {e}"))
        finally:
            conn.close()

def add_diary_entry (telegram_id , content ):
    conn = create_connection()
    if conn:
        try:
            # Получаем user_created_at из таблицы users
            cursor = conn.cursor()
            cursor.execute("SELECT created_at FROM users WHERE telegram_id = ?", (telegram_id,))
            user_created_at = cursor.fetchone()
            if user_created_at:
                user_created_at = user_created_at[0]
            else:
                print("Пользователь не найден")
                return None

            # Добавление новой записи в дневник
            sql = "INSERT INTO diary_entries (telegram_id, content) VALUES (?, ?)"
            cursor.execute(sql, (telegram_id, content))
            entry_id = cursor.lastrowid
            conn.commit()
            print("Запись успешно добавлена")

            # Логирование действия
            add_audit_log(
                telegram_id=telegram_id,
                action="added_diary_entry",
                user_created_at=user_created_at,
                entry_created_at=datetime.now(),
                new_content=content,
                phone_number=None  # Если номер не нужен
            )
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
            cursor.execute("SELECT * FROM diary_entries WHERE telegram_id = ? AND DATE(date) = DATE(?)", (telegram_id, date))
            entries = cursor.fetchall()

            # Проверяем, есть ли записи
            if entries:
                print("\nВаши записи:")
                for entry in entries:
                    print(f"ID записи: {entry[0]}, Дата: {entry[2]}, Запись: {entry[3]}")
                    print(f"Запомните ваш ID {entry[0]} записи, если захотите изменить запись или удалить ее!")
            else:
                print("Записей за указанную дату не найдено.")

        except sqlite3.Error as e:
            print(f"Произошла ошибка {e}")
        finally:
            conn.close()


def filter_diary_by_date_range (telegram_id, date_start, date_end):
    conn=create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM diary_entries WHERE telegram_id = ? AND DATE(date) BETWEEN DATE(?) AND DATE(?)", (telegram_id, date_start, date_end))
            entries = cursor.fetchall()
            if entries:
                print("\nВаши записи:")
                for entry in entries:
                    print(f"ID записи: {entry[0]}, Дата: {entry[2]}, Запись: {entry[3]}")
                    print(f"Запомните ваш ID {entry[0]} записи, если захотите изменить запись или удалить ее!")
            else:
                print("Записей за указанный период не найдено.")
        except sqlite3.Error as e:
            print(f"Произошла ошибка {e}")
        finally:
            conn.close()


def update_diary_entry(telegram_id, entry_id, new_content):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Получаем старое содержание для логирования
            cursor.execute("SELECT content, date FROM diary_entries WHERE telegram_id = ? AND entry_id = ?",
                           (telegram_id, entry_id))
            entry = cursor.fetchone()

            if entry:
                old_content = entry[0]
                entry_created_at = entry[1]

                # Обновление содержания записи
                cursor.execute(
                    "UPDATE diary_entries SET content = ? WHERE entry_id = ? AND telegram_id = ?",
                    (new_content, entry_id, telegram_id)
                )
                conn.commit()

                if cursor.rowcount > 0:
                    print("\nЗапись успешно обновлена.")
                    # Добавляем лог действия
                    add_audit_log(
                        telegram_id=telegram_id,
                        action="update_diary_entry",
                        user_created_at=None,  # Если user_created_at не нужен, можно убрать
                        entry_created_at=entry_created_at,
                        old_content=old_content,
                        new_content=new_content,
                        phone_number=None  # Уберите, если не требуется
                    )
                else:
                    print("Запись с таким ID не найдена.")
            else:
                print("Запись не найдена.")
        except sqlite3.Error as e:
            print(f"Произошла ошибка {e}")
        finally:
            conn.close()


def delete_user(telegram_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
            entry = cursor.fetchone()
            if entry:
                entry_created_at =  entry[2]
                phone_number = entry[3]
                old_content = entry[4]

                cursor.execute("DELETE FROM users WHERE telegram_id = ?", (telegram_id,))
                cursor.execute("DELETE FROM diary_entries WHERE telegram_id = ?", (telegram_id,))
                conn.commit()
                print("Запись успешно удалена")
                add_audit_log(
                    telegram_id=telegram_id,
                    action="delete_user",
                    user_created_at=None,  # Если user_created_at не нужен, можно убрать
                    entry_created_at=entry_created_at,
                    old_content=old_content,
                    new_content=None,
                    phone_number=phone_number
                )
            else:
                print("Запись с таким ID не найдена.")
        except sqlite3.Error as e:
            print(f"Произошла ошибка {e}")
        finally:
            conn.close()
