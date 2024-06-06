from pprint import pprint

q = '''
Контекстный менеджер в Python - это объект, который определяет вход и выход из контекста с помощью методов enter() и exit().

Literal - от английского "literally", то есть "буквально".

Метаклассы - это классы, которые определяют поведение других классов.

Ктотофлоу, канбан, эджайл --> скрам -- методология косанды, покер планиров
'''
# print(q)
lines = q.split('\n')
# print(lines)

text = [ i.strip('') for i in lines if i.strip()]
pprint(text)



# import asyncio
# import aioschedule
#
#
# @dp.message_handler()
# async def choose_your_dinner():
#     for user in set(the_users_without_dinner()):
#         await bot.send_message(chat_id=user, text="Хей🖖 не забудь выбрать свой ужин сегодня
#         ", reply_markup = menu_garnish)
#
#         async def scheduler():
#             aioschedule.every().day.at("17:45").do(choose_your_dinner)
#         while True:
#             await aioschedule.run_pending()
#             await asyncio.sleep(1)
#
#     async def on_startup(dp):
#         asyncio.create_task(scheduler())
#
#     if __name__ == '__main__':
#         executor.start_polling(on_startup=on_startup)