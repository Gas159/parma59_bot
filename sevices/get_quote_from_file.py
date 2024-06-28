import random
from typing import Generator
from config import config


def generic_get_quote(file_path: str) -> Generator[str, None, None]:
	try:
		with open(file_path, 'r') as file:
			raw_text = file.read()
			clear_text = [item.strip() for item in raw_text.split('\n\n') if item.strip()]
			for item in shuffle(clear_text):
				yield item
	except FileNotFoundError:
		print(f"File '{file_path}' not found.")
	except Exception as e:
		print(f"An error occurred: {e}")


def shuffle(string: list):
	random.shuffle(string)
	return string


# print(config.BASE_DIR)
print(config.FILE_PATH)

get_quote = generic_get_quote(config.FILE_PATH)
# print(next(get_quote))
# print(next(get_quote))

