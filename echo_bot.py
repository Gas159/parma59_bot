import asyncio
import logging

import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
BOT_TOKEN: str = os.getenv('BOT_TOKEN')
bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()

logging.basicConfig(level=logging.INFO)
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
API_URL = 'https://api.telegram.org/bot'
ERROR_TEXT = 'Здесь должна была быть картинка с котиком :('

list_of_chats: dict[str, int] = {'pdd': -1002097028485,
                                 'parma': -1002020818544}

test_chats: dict[str, int] = {'test_1': -4161841389,
                              'test_2': -4155526550, }

date_of_caption = {'date': ''}


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=["help"]))
async def process_start_command(message: Message):
    await message.answer('Начни предложение/подпись фото с "!" чтобы отправить его в др группу.\n ')


@dp.message(F.text.lower().startswith(("й", 'q', 'cat', "кот")))
async def send_echo_cat(message: Message):
    try:
        cat_response = requests.get(API_CATS_URL)
        print(cat_response, type(cat_response))
        # print(message.model_dump_json(indent=4, exclude_none=True))
        if cat_response.status_code == 200:
            cat_link = cat_response.json()[0]['url']
            print(cat_response.json())
            await message.answer_photo(photo=cat_link)
        #     requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={message.chat.id}&photo={cat_link}')
        else:
            await message.answer(text=ERROR_TEXT)
            # requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={message.chat.id}&text={ERROR_TEXT}')
    except Exception as e:
        logging.exception(e)


@dp.message(F.text.startswith("!"), lambda msg: len(msg.text) > 1)
async def send_text_test(message: Message):
    try:
        print(message.model_dump_json(indent=4, exclude_none=True))
        for name, chat_id in list_of_chats.items():
            if not chat_id == message.chat.id:
                await bot.send_message(chat_id=chat_id, text=message.text[1:])
        await message.answer(text=f"Сообщение отправлено.")
    except Exception as e:
        logging.exception(e)


async def send_file(msg: Message):
    for chat_name, chat_id in list_of_chats.items():
        if not chat_id == msg.chat.id:
            await msg.copy_to(chat_id=chat_id)
    await msg.answer(text=f"Файл отправлен.")


@dp.message(F.photo | F.document)
async def send_photo_test(message: Message):
    try:
        if message.caption and message.caption.startswith('!'):
            date_of_caption['date'] = message.date
            await send_file(message)

        elif date_of_caption['date'] == message.date:
            await send_file(message)

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
