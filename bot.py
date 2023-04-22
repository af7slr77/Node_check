import time
from config import token_bot, chat_id
from aiogram import Bot, Dispatcher, executor, types
import asyncio
from main import get_nodes_info
bot = Bot(token=token_bot)
dp = Dispatcher(bot)

messages_id_data = []
comands_name_data = [
	'zilliqa',
	'rockx',
	'ezil.me',
	'wave',
	'shardpool.io',
	'valkyrie2',
	'huobi staking',
	'zilliqa2',
	'moonlet.io',
	'bountyblok',
	'everstake.one',
	'nodamatics.com',
	'zilpay',
	'avely finance',
	'viewblock',
	'atomicwallet',
	'binance staking',
	'luganodes',
	'cex.io',
	'blox-sdk staking',
	'valkyrie investments',
	'ignite dao',
	'zillet',
	'staked',
	'kucoin',
	'hashquark',
	'stakin']


@dp.message_handler()
async def start(message: types.Message):
	user_id = message.from_user.id
	node_for_tracking = message.text
	while True:
		await check_nodes(user_id, node_for_tracking)
		# await clear_chat() 
	




async def check_nodes(user_id, node_for_tracking):
	responce = await get_nodes_info()
	for i in responce:
		if i['name'].lower() == node_for_tracking.lower():
			if i['current_dse_poch'] == 'error' or i['current_mini_epoch'] == 'error':
				msg = i['name'] + ' ' + 'something went wrong, check the node!'
				send_message = await bot.send_message(user_id, msg)
				message_id = send_message['message_id']
				messages_id_data.append(message_id)
			else:
				msg = i['current_dse_poch'] + ' ' + i['current_mini_epoch']
				await bot.send_message(user_id, msg)
	# else:
	# 	msg = 'Node does not exist! Please try again'
	# 		await bot.send_message(user_id, msg)



async def clear_chat(): # Deletes all messages from the chat except the last 6
	if messages_id_data:
		for id in messages_id_data[:-30]:
			await bot.delete_message(chat_id, id)
			messages_id_data.remove(id)


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.create_task(get_nodes_info())
	executor.start_polling(dp)