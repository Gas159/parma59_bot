import asyncio
import logging
import sys
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram import F

from dotenv import load_dotenv
import os

from sevices.get_quote_from_file import get_quote

load_dotenv()  # take1234567891 environment variables from .env.

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather1
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
                              'test_2': -4155526550,
                              'test_plus': -4213163596,
                              'need_to_pump_up': -4231461902}

list_of_records = ['1', '2', '3', '4', '5']

pluses = {
	'Гас': {'user_id': 1363407847, 'msg': None, 'chat_id': -4155526550},
	'Полина': {'user_id': 5150369451, 'msg': None, 'chat_id': None},
	'Влад': {'user_id': 2082981840, 'msg': None, 'chat_id': None}
}


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


# send "ahtung" if not plus every day
@dp.message(F.text.lower().startswith("+"))
async def send_msg(message: Message):
	try:
		# print(message.model_dump_json(indent=4, exclude_none=True))
		for user in pluses:
			print(user)
			if user == message.from_user.first_name:
				pluses[user]['msg'] = message.text
				pluses[user]['user_id'] = message.from_user.id
				pluses[user]['chat_id'] = message.chat.id
		print(pluses)
		await bot.send_message(chat_id=-4155526550, text='Check of "+"')
	except Exception as e:
		logging.exception(e)


async def send_msg_if_not_plus():
	try:
		# print(message.model_dump_json(indent=4, exclude_none=True))
		for user in pluses:
			print(user, type(user))
			print(pluses)
			if not pluses[user]['msg']:
				# send msg tp test2
				await bot.send_message(chat_id=-4155526550, text=f'{user} плюс поставь!')
	except Exception as e:
		logging.exception(e)


async def delete_plus():
	for user in pluses:
		pluses[user]['msg'] = None
	await bot.send_message(chat_id=-4155526550, text='Plus was delete')


@dp.message(F.text.startswith("1"))  # lambda msg: len(msg.text) > 1
async def send_text_test(message: Message):
	try:
		print(message.model_dump_json(indent=4, exclude_none=True))
		phrase = next(get_quote)
		print(type(phrase), phrase)
		# await message.answer(text=f"Сообщение отправлено.")отправлено
		await message.answer(text=phrase)
	except Exception as e:
		logging.exception(e)


async def send_message1(chat_id: int):
	"""Функция для отправки сообщения пользователю."""
	try:

		phrase = next(get_quote)
		print(type(phrase), phrase)
		await bot.send_message(chat_id=chat_id, text=phrase)
		logging.info("Message sent successfully")
	except Exception as e:
		logging.error(f"Error sending message: {e}")


@dp.message(F.text.startswith('id'))
async def get_id(message: Message):
	print('111111111111111')
	user_id = message.from_user.id
	chat_id = message.chat.id
	user_name = message.from_user.first_name
	await message.answer(f"user ID: {user_id} \nchat ID: {chat_id} \nname: {user_name}")


async def main() -> None:
	# Удаление вебхука
	await bot.delete_webhook(drop_pending_updates=True)

	#
	# time_zone = timezone("Europe/Moscow")
	# current_timezone = time_zone + timedelta(hours=2)
	# print(current_timezone)
	scheduler = AsyncIOScheduler(timezone='Etc/GMT+5')

	scheduler.add_job(send_message1, trigger="interval", hours=12, seconds=5, start_date=datetime.now(), kwargs={
		# "bot": bot,
		# "chat_id": -4161841389
		'chat_id': test_chats['need_to_pump_up']
	}, )

	# scheduler.add_job(send_msg_if_not_plus, trigger="interval", seconds=10, start_date=datetime.now(), kwargs={
	#     "bot": bot,
	# })

	scheduler.add_job(send_msg_if_not_plus, trigger="cron", hour='10,11,21,22,23', minute=30, kwargs={
		# "bot": bot,
	}, )
	scheduler.add_job(delete_plus, trigger="cron", hour=23, minute=50, kwargs={
		# "bot": bot,
	}, )
	# print(datetime.now())

	scheduler.start()
	logging.debug(scheduler)
	await dp.start_polling(bot)


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	asyncio.run(main())

# async def delete_webhook_and_handle_updates():
#     # Удаление вебхука
#     await bot.delete_webhook(drop_pending_updates=True)
#
#     # Начало обработки обновлений через периодический опрос
#     await dp.start_polling(bot)
