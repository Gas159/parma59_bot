import asyncio
import logging
import random

import aioschedule
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

from dotenv import load_dotenv
import os
from test1 import text

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

list_of_records = ['1', '2', '3', '4', '5']


def shuffle(lst):
    random.shuffle(lst)
    for i in lst:
        yield i


date_of_caption = {'date': ''}

q = '''
Контекстный менеджер в Python - это объект, который определяет вход и выход из контекста с помощью методов enter() и exit().

Literal - от английского "literally", то есть "буквально".

Метаклассы - это классы, которые определяют поведение других классов.

Ктотофлоу, канбан, эджайл --> скрам -- методология косанды, покер планиров

Да уж , тут не до веселья , когда дед Егор, прогуливая уроки и сколопендру - нечаяно получил получку и рекошетом в лоб 
!!! "Да, все устраивает" !!! - подумали соседи и не стали делать ему поп-корн  !!!! Простите , специи в плове нынче - ТЕ!!!!!
'''
# print(q)
lines = q.split('\n')
# print(lines)

text = [i.strip('') for i in lines if i.strip()]


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
        for name, chat_id in test_chats.items():
            if not chat_id == message.chat.id:
                await bot.send_message(chat_id=chat_id, text=message.text[1:])
        await message.answer(text=f"Сообщение отправлено.")
    except Exception as e:
        logging.exception(e)


@dp.message(F.text.startswith("1"))  # lambda msg: len(msg.text) > 1
async def send_text_test(message: Message):
    try:
        print(message.model_dump_json(indent=4, exclude_none=True))
        phrase = next(shuffle(text))
        # await message.answer(text=f"Сообщение отправлено.")отправлено
        await message.answer(text=phrase)
    except Exception as e:
        logging.exception(e)


async def scheduler():
    # aioschedule.every().day.at("17:45").do(send_text_test1)
    aioschedule.every(3).seconds.do(send_text_test1)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def send_text_test1(message: Message=None):
    try:
        # print(message.model_dump_json(indent=4, exclude_none=True))
        phrase = next(shuffle(text))
        # await message.answer(text=f"Сообщение отправлено.")отправлено
        await message.answer(text=phrase)
    except Exception as e:
        logging.exception(e)


async def on_startup():
    asyncio.create_task(scheduler())




async def send_file(msg: Message):
    for chat_name, chat_id in test_chats.items():
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


# @dp.message(F.photo | F.document)
# async def send_photo_test(message: Message):
#     try:
#         # print()
#         # print(message.model_dump_json(indent=4, exclude_none=True))
#         print(message.caption, type(message.caption))
#         print(message.message_id)
#         print('eto date of caption: ', date_of_caption['date'])
#         print('eto message date: ', message.date)
#         print()
#         print('Step without caption: ', date_of_caption['date'])
#         print('Step without caption: ', date_of_caption['date'] == message.date)
#         print('Eto update_id: ', message.message_id)
#
#         if date_of_caption['date'] == message.date:
#             for chat_name, chat_id in test_chats.items():
#                 if not chat_id == message.chat.id:
#                     await message.copy_to(chat_id=chat_id)
#                     print('!!!')
#             await message.answer(text=f"Файл отправлен.")
#
#     except Exception as e:
#         logging.exception(e)


async def delete_webhook_and_handle_updates():
    # Удаление вебхука
    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup(bot)
    # Начало обработки обновлений через периодический опрос
    await dp.start_polling(bot, on_startup=on_startup)


# Запуск асинхронной функции
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delete_webhook_and_handle_updates())
