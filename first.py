

import requests
import time

from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.

API_URL = 'https://api.telegram.org/bot'
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
TEXT = 'Ура! Классный апдейт!'
ERROR_TEXT = 'Здесь должна была быть картинка с котиком :('
MAX_COUNTER = 100

offset = -2
counter = 0
cat_response: requests.Response
cat_link: str
# chat_id: int

while counter < 100:
    print('attempt =', counter)
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
    print(updates)

    if updates['result']:
        for result in updates['result']:
            print(result)
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            cat_response = requests.get(API_CATS_URL)
            print(cat_response, type(cat_response))
            if cat_response.status_code == 200:
                # cat_link = cat_response.json()[0]['url']
                # *cat_link,fd = cat_response.json()
                cat_link = cat_response.json()[0]['url']
                print(cat_response.json())
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

    time.sleep(1)
    counter += 1
