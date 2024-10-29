import sqlite3

from database.connection import create_connection

conn = create_connection()
if conn:
    try:
        cursor = conn.cursor()

        # Извлекаем данные из таблицы users с названиями полей
        cursor.execute(
            "SELECT users_id as 'ID', telegram_id as 'Telegram ID', username as 'Имя пользователя', phone_number as 'Номер телефона', created_at as 'Дата создания' FROM users")
        users = cursor.fetchall()  # Извлекаем все записи для удобного вывода
        print("\nСодержание таблицы users:")

        # Получаем имена столбцов
        user_columns = [description[0] for description in cursor.description]
        print(" | ".join(user_columns))  # Выводим заголовок столбцов

        for user in users:
            print(user)

        # Извлекаем данные из таблицы diary_entries с названиями полей
        cursor.execute(
            "SELECT entry_id as 'ID записи', telegram_id as 'Telegram ID', date as 'Дата записи', content as 'Содержание записи' FROM diary_entries")
        entries = cursor.fetchall()  # Извлекаем все записи для удобного вывода
        print("\nСодержание таблицы diary_entries:")

        # Получаем имена столбцов
        entry_columns = [description[0] for description in cursor.description]
        print(" | ".join(entry_columns))  # Выводим заголовок столбцов

        for entry in entries:
            print(entry)

    except sqlite3.Error as e:
        print(f"Произошла ошибка {e}")
    finally:
        conn.close()

