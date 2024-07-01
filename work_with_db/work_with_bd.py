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


def get_text(file_path: str) -> list[str]:
	with open(file_path, 'r') as file:
		text = file.read()
		lst = [item.strip() for item in text.split('\n\n') if item.strip()]
		print(lst)
		return lst


def shuffle(string: list):
	random.shuffle(string)
	return string


def connect_to_db() -> None:
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
			print('Record added')
	except psycopg2.Error as e:
		print(f'Error: {e}')


def del_all_records_from_db() -> None:
	conn = connect_to_db()
	try:
		with conn.cursor() as cur:
			cur.execute('delete from quotes *')
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


def select_random_queto_from_db() -> None:
	conn = connect_to_db()
	try:
		with conn.cursor() as cur:

			cur.execute('select q.id, q.quote from quotes as q'
			            ' left join used_quotes_id as uq on q.id = uq.used_id '
			            'where uq.used_id is null '
			            'order by random() limit 1')
			rows = cur.fetchall()
			print(rows)
			print(rows[0][0], rows[0][1])
			cur.execute("insert into used_quotes_id (used_id) values (%s)", (rows[0][0],))
			conn.commit()
			# cur.execute("INSERT INTO quotes (user_name, quote) VALUES (%s, %s)", (user_name, record))
			# conn.commit()
			# print(f' name: {rows[0][0]} quote: {rows[0][1]} id: {rows[0][2]}')
			return '. '.join([str(rows[0][0]), rows[0][1]])

	except psycopg2.Error as e:
		print(f'Error1: {e}')


if __name__ == '__main__':
	# del_all_records_from_db()
	# add_record_to_db()
	# select_all_from_db()
	# select_id_from_db()
	add_records_to_db_from_file('test_record')
	# select_random_queto_from_db()
