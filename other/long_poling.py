

import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
BOT_TOKEN = os.getenv('BOT_TOKEN')


API_URL = 'https://api.telegram.org/bot'
offset = -2
timeout = 60
updates: dict


def do_something() -> None:
    print('Был апдейт')


while True:
    start_time = time.time()
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}&timeout={timeout}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            do_something()

    end_time = time.time()
    print(f'Время между запросами к Telegram Bot API: {end_time - start_time}')