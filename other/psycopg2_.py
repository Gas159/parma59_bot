import psycopg2
# improt from .env
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')


# BOT_TOKEN: str = os.getenv('BOT_TOKEN')

def main():
	# Connect to the database
	try:
		with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST) as conn:
			print(conn)
			# Create a cursor
			with conn.cursor() as cur:
				q = 1
				# Create a new record
				cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("value1",q))

				# Commit the changes
				conn.commit()

				# View data
				cur.execute("SELECT * FROM users")
				rows = cur.fetchall()
				for row in rows:
					print(row)
	except psycopg2.Error as e:
		print(f'Error: {e}')

		# def main():
		# 	# Подключение к базе данных
		# 	conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
		#
		#
		# 	print(conn)
		# 	# Создание курсора
		# 	cur = conn.cursor()
		#
		# 	# Создание новой записи
		# 	cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("value1", 32))
		#
		# 	# Фиксация изменений
		# 	conn.commit()
		#
		# 	# view data
		# 	cur.execute("SELECT * FROM users")
		# 	rows = cur.fetchall()
		# 	for row in rows:
		# 		print(row)
		#
		# 	# Закрытие курсора и соединения
		# 	cur.close()
		# 	conn.close()

if __name__ == '__main__':
	main()
