import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="testdb",
    user="testuser",
    password="123",
    host="localhost"
)

# Создание курсора
cur = conn.cursor()

# Создание новой записи
cur.execute("INSERT INTO mytable (column1, column2) VALUES (%s, %s)", ("value1", "value2"))

# Фиксация изменений
conn.commit()

# Закрытие курсора и соединения
cur.close()
conn.close()

