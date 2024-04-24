import asyncio
import logging

import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram import F
# from aiogram.utils import executor

from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
API_URL = 'https://api.telegram.org/bot'
ERROR_TEXT = 'Здесь должна была быть картинка с котиком :('
# Этот хэндлер будет срабатывать на команду "/start"
# @dp.message(Command(commands=["start"]))
# async def process_start_command(message: Message):
#     await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')
#
#
# # Этот хэндлер будет срабатывать на команду "/help"
# @dp.message(Command(commands=['help']))
# async def process_help_command(message: Message):
#     await message.answer(
#         'Напиши мне что-нибудь'
#     )


list_of_chats = {'test': -4161841389,
                 'pdd': -1002097028485,
                 'parma': -1002020818544}


@dp.message(F.text.startswith(("й", "Й")))
async def send_echo(message: Message):
    try:
        cat_response = requests.get(API_CATS_URL)
        print(cat_response, type(cat_response))
        if cat_response.status_code == 200:
            cat_link = cat_response.json()[0]['url']
            print(cat_response.json())
            # chat_id = result['message']['from']['id']
            # await bot.send_message(chat_id=massage.chat.id, text=message.text[1:])
            # await message.answer()
            requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={message.chat.id}&photo={cat_link}')
        else:
            requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={message.chat.id}&text={ERROR_TEXT}')
        #     requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')
    except Exception as e:
        logging.exception(e)


@dp.message(F.text.startswith(("!", "й", "Й")), lambda msg: len(msg.text) > 1)
async def send_echo(message: Message):
    try:

        # logging.info('hi')
        print(message.model_dump_json(indent=4, exclude_none=True))
        for name, chat_id in list_of_chats.items():
            if not chat_id == message.chat.id:
                await bot.send_message(chat_id=chat_id, text=message.text[1:])
        await message.answer(text=f"Сообщение отправлено.")
    except Exception as e:
        logging.exception(e)


@dp.message(F.photo | F.document)
async def send_photo(message: Message):
    try:
        print()
        print(message.model_dump_json(indent=4, exclude_none=True))
        print()
        # if message.caption and message.caption.startswith('!'):
        for chat_name, chat_id in list_of_chats.items():
            if not chat_id == message.chat.id:
                await message.copy_to(chat_id=chat_id)
        await message.answer(text=f"Файл отправлен.")
    except Exception as e:
        logging.exception(e)


async def delete_webhook_and_handle_updates():
    # Удаление вебхука
    await bot.delete_webhook(drop_pending_updates=True)

    # Начало обработки обновлений через периодический опрос
    await dp.start_polling(bot)


# Запуск асинхронной функции
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delete_webhook_and_handle_updates())

# if __name__ == '__main__':
#     dp.run_polling(bot, skip_updates=True)

# async def delete_webhook_and_handle_updates():
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.run_polling(bot)
#
#
# if __name__ == '__main__':
#     # loop = asyncio.get_event_loop()
#     # loop.run_until_complete(delete_webhook_and_handle_updates())
#     delete_webhook_and_handle_updates()
