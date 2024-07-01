import random

import psycopg2
from dotenv import load_dotenv
import os
from config.config import FILE_PATH

load_dotenv()  # take environment variables from .env
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
FILE_PATH = FILE_PATH

DB_NAME_REMOTE = 'gasdb'
DB_USER_REMOTE = 'gas'
DB_PASSWORD_REMOTE = '123'
DB_HOST_REMOTE = 'localhost'
# DB_HOST_REMOTE = '45.9.73.213'


def get_text(file_path: str) -> list[str]:
	with open(file_path, 'r') as file:
		text = file.read()
		lst = [item.strip() for item in text.split('\n\n') if item.strip()]
		print(lst)
		return lst


def shuffle(string: list):
	random.shuffle(string)
	return string


def connect_to_db() -> psycopg2.connect:
	try:
		with (psycopg2.connect(dbname=DB_NAME_REMOTE, user=DB_USER_REMOTE, password=DB_PASSWORD_REMOTE,
		                       host=DB_HOST_REMOTE)
		      as conn):
			return conn
	except psycopg2.Error as e:
		print(f'Error: {e}')


def connect_to_db1() -> psycopg2.connect:
	try:
		with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST) as conn:
			return conn
	except psycopg2.Error as e:
		print(f'Error: {e}')


def add_records_to_db_from_file(user_name: str = 'Gas') -> None:
	try:
		conn = connect_to_db()
		with conn.cursor() as cur:
			for record in get_text(FILE_PATH):
				print(str(record))
				cur.execute("INSERT INTO quotes (user_name, quote) VALUES (%s, %s)", (user_name, record))
			conn.commit()
			print('All records from file added')
	except psycopg2.Error as e:
		print(f'Error: {e}')


def add_record_to_db(record: str = 'Default', user_name: str = 'Gas') -> None:
	try:
		conn = connect_to_db()
		with conn.cursor() as cur:
			cur.execute("INSERT INTO quotes (user_name, quote) VALUES (%s, %s)", (user_name, record))
			conn.commit()
			cur.execute('select id from quotes where quote = %s', (record,))
			print('Record added')
			result = cur.fetchone()[0]
			return result
	except psycopg2.Error as e:
		print(f'Error: {e}')


def del_all_records_from_db(table: str) -> None:
	conn = connect_to_db()
	try:
		with conn.cursor() as cur:
			cur.execute(f'delete from {table} *')
			conn.commit()
			print('All records deleted')
	except psycopg2.Error as e:
		print(f'Error: {e}')


def select_all_from_db() -> None:
	conn = connect_to_db()
	try:
		with conn.cursor() as cur:
			cur.execute("SELECT * FROM quotes")
			rows = cur.fetchall()
			for row in rows:
				print(row)
	except psycopg2.Error as e:
		print(f'Error: {e}')


def select_id_from_db() -> list:
	conn = connect_to_db()
	try:
		with conn.cursor() as cur:
			cur.execute("select id from quotes")
			ids = cur.fetchall()

			ids_clear = []
			for _id in ids:
				ids_clear.append(*_id)
			shuffle(ids_clear)
			print(ids_clear)
			return ids_clear
	except psycopg2.Error as e:
		print(f'Error: {e}')


def select_random_quote_from_db() -> str:
	conn = connect_to_db()
	try:
		with conn.cursor() as cur:

			cur.execute('select q.id, q.quote from quotes as q '
			            'where q.published is not true or published is null '
			            'order by random() limit 1')

			# cur.execute('select q.id, q.quote from quotes as q'
			#             'where published is not true '
			#             'order by random() limit 1')
			rows = cur.fetchall()
			# if not rows:
			# 	del_all_records_from_db('used_quotes_id')
			print(rows)
			print(rows[0][0], rows[0][1])
			if not rows:
				cur.execute('update quotes set published = true')
			cur.execute("update quotes set published = true where id = %s", (rows[0][0],))
			conn.commit()

			# cur.execute("INSERT INTO quotes (user_name, quote) VALUES (%s, %s)", (user_name, record))
			# conn.commit()

			return '. '.join([str(rows[0][0]), rows[0][1]])
	except psycopg2.Error as e:
		print(f'Error: {e}')


def get_quote_from_db(id_: int) -> str:
	conn = connect_to_db()
	try:
		with conn.cursor() as cur:
			cur.execute('SELECT q.id, q.quote FROM quotes as q WHERE id = %s', (id_,))
			row = cur.fetchone()
			print(row)
			if row:
				return row[1]
			else:
				return "Quote not found"
	except psycopg2.Error as e:
		print(f'Error: {e}')


if __name__ == '__main__':
	# del_all_records_from_db('quotes')
	# add_record_to_db("blabla\nblalba")
	# select_all_from_db()
	# select_id_from_db()
	# add_records_to_db_from_file()
	select_random_quote_from_db()
	print(get_quote_from_db(1))
