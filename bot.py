import time
from config import token_bot, chat_id
from aiogram import Bot, Dispatcher, executor, types
import asyncio
from main import get_nodes_info
bot = Bot(token=token_bot)
dp = Dispatcher(bot)

messages_id_data = [] # store messages id


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	user_id = message.from_user.id
	if user_id in user_id_data:
		print("this user is already logged in")
	else:
		user_id_data.append(user_id)
		
	


async def check_nodes():
	responce = await get_nodes_info()
	print(responce)
	for i in responce:
		if i['current_dse_poch'] == 'error' or i['current_mini_epoch'] == 'error':
			msg = i['name'] + ' ' + 'something went wrong, check the node!'
			send_message = await bot.send_message(chat_id, msg)
			message_id = send_message['message_id']
			messages_id_data.append(message_id)



async def clear_chat(): # Deletes all messages from the chat except the last 6
	if messages_id_data:
		for id in messages_id_data[:-30]:
			await bot.delete_message(chat_id, id)
			messages_id_data.remove(id)



async def main():

	while True:
		await check_nodes()
		await clear_chat() 
		# await asyncio.sleep(225)


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.create_task(main())
	executor.start_polling(dp)