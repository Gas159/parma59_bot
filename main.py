import asyncio
import logging
import sys
from datetime import datetime

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram import F

from dotenv import load_dotenv
import os

from pytz import timezone

from sevices.get_quote_from_file import get_quote

GROUP_PLUS_CHAT_ID = -1002187451337  # Замените на ID вашей группы
Test_chat_for_plus = -4155526550
REPORT_CHAT_ID = -4155526550  # Замените на ID чата для отчётов

load_dotenv()  # take1234567891 environment variables from .env.

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather1
BOT_TOKEN: str = os.getenv('BOT_TOKEN')
bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()

logging.basicConfig(level=logging.INFO)
API_URL = 'https://api.telegram.org/bot'


# Хранилище для участников и их плюсов
pluses = {}


async def send_report():
    while True:
        now = datetime.now()
        # Проверяем, если сейчас 18:00
        if now.hour == 23 and now.minute == 59:
            # Формируем отчет
            missed_users = [user for user in pluses if pluses[user] == False]

            if missed_users:
                report_message = "Не поставили плюс: " + ", ".join(missed_users)
                await bot.send_message(REPORT_CHAT_ID, report_message)
            else:
                await bot.send_message(REPORT_CHAT_ID, "Все поставили плюс!")
            await asyncio.sleep(60)  # Ждём 1 минуту, чтобы не отправлять несколько сообщений в минуту
        await asyncio.sleep(30)  # Проверяем каждую 30 секунд


async def send_msg_if_not_plus(bot: Bot):
	try:
		current_time = datetime.now().strftime("%H:%M:%S")
		print(current_time)
		await bot.send_message(chat_id=-4155526550, text=f'Плюс поставь! at {current_time}.\nmy set '
		                                                 f'time is 10:30:00')
	except Exception as e:
		logging.exception(e)



@dp.message(F.text.startswith('id'))
async def get_id(message: Message):
	print('111111111111111')
	user_id = message.from_user.id
	chat_id = message.chat.id
	user_name = message.from_user.first_name
	await message.answer(f"user ID: {user_id} \nchat ID: {chat_id} \nname: {user_name}")


@dp.message(F.text)
async def handle_plus(message: types.Message):
	user_id = message.from_user.username or message.from_user.id
	# if message.text and message.chat.id == GROUP_PLUS_CHAT_ID:
	if message.text and message.chat.id == Test_chat_for_plus:
		print(message.text)
		print(message.chat.id)
		# pluses[user_id] = True
		print(pluses)
		await message.reply("Плюс принят!")


async def main() -> None:
	# Удаление вебхука
	await bot.delete_webhook(drop_pending_updates=True)
	timezone = pytz.timezone('Europe/Moscow')
	# scheduler = AsyncIOScheduler(timezone='Etc/GMT+5')
	scheduler = AsyncIOScheduler()
	#
	# scheduler.add_job(send_msg_if_not_plus, trigger="interval", hours=0, seconds=5, start_date=datetime.now(),
	#                   kwargs={"bot": bot}, ) #timezone=timezone

	scheduler.start()
	logging.debug(scheduler)
	await dp.start_polling(bot)


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	# Инициализируем хранилище
	for user_id in pluses.keys():
		pluses[user_id] = False  # Устанавливаем начальное значение для всех пользователей
	asyncio.run(main())
