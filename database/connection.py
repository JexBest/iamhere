import sqlite3

def create_connection(database="data.db"):
    """Создает и возвращает подключение к базе данных."""
    conn = None
    try:
        conn = sqlite3.connect(database)
        print("Успешное подключение к БД")
    except sqlite3.Error as e:
        print(f"Ошибка подключения к БД: {e}")
    return conn
if __name__ == "__main__":
    create_connection()