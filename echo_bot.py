from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


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


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message(F.text.startswith("!") & len(F.text)>1)
async def send_echo(message: Message):
    # await bot.send_message(chat_id='ID или название чата', text='Какой-то текст')
    # print(message)
    # await bot.send_message(chat_id=message.chat.id, text=message.text)
    current_chat_id = message.chat.id
    #print('Current chat id')
    # print(current_chat_id, type(current_chat_id))
    #print(type(message.text))
    print(message.text)
    if message.text:

        if message.text.startswith('!') and:
            # if message.text
            for k, v in list_of_chats.items():

                if not v == current_chat_id:
                    print(type(message.text))

                    await bot.send_message(chat_id=v, text=message.text[1:])
                else:
                    await message.answer(chat_id=v, text='Message sent')
                # await message.reply(text=(message.text + ' ' + str(message.chat.id)))


if __name__ == '__main__':
    dp.run_polling(bot)
    #print('Running')
