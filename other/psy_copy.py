import psycopg2
from typing import List, Tuple

def main(dbname: str, user: str, password: str, host: str) -> None:
    """
    Connects to a PostgreSQL database, inserts a new record into the 'users' table,
    and prints all records in the 'users' table.

    Args:
        dbname (str): The name of the database.
        user (str): The username for the database connection.
        password (str): The password for the database connection.
        host (str): The hostname for the database connection.

    Returns:
        None
    """
    # Подключение к базе данных
    conn: psycopg2.extensions.connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    print(conn)
    # Создание курсора
    cur: psycopg2.extensions.cursor = conn.cursor()

    # Создание новой записи
    cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("value1", 32))

    # Фиксация изменений
    conn.commit()

    # view data
    cur.execute("SELECT * FROM users")
    rows: List[Tuple[str, int]] = cur.fetchall()
    for row in rows:
        print(row)

    # Закрытие курсора и соединения
    cur.close()
    conn.close()

main() # Запуск программы