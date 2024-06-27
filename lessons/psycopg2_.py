import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
	dbname="testdb",
	user="testuser",
	password="123",
	host="localhost"
)
print(conn)
# Создание курсора
cur = conn.cursor()

# Создание новой записи
cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("value1", 32))

# Фиксация изменений
conn.commit()

#view data
cur.execute("SELECT * FROM users")
rows = cur.fetchall()
for row in rows:
    print(row)


# Закрытие курсора и соединения
cur.close()
conn.close()
