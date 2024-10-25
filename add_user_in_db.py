import sqlite3


def connect_to_bd (database):
    conn = None
    try:
        conn = sqlite3.connect(database)
        print("Мы успешно подключились к БДшечке")
    except sqlite3.Error as e:
        print(f"Произошла ошибка {e}")
    return conn




def create_user (database):



if __name__ == "__main__":
    data_file = "data.db"
    conn = connect_to_bd(data_file)
    if conn is not None:
        create_user(data_file)
        conn.close()