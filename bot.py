import asyncio
from config import token_bot
from aiogram import Bot, Dispatcher, executor, types
from keyboard import kb
from main import get_nodes_info
from datetime import datetime
from models import db, nodes,connection, write_to_db, get_all_recors, update, get_recording_from_database


bot = Bot(token=token_bot)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
	user_id = message.from_user.id
	msg = 'Hi! I am a bot for tracking nodes of Zilliqa. Press "/help" for help' 
	await bot.send_message(user_id, msg, reply_markup=kb)

@dp.message_handler(commands=["help"])
async def help_comand(message: types.Message):

	msg = """
	Nodes available for tracking:
	<b>zilliqa '</b>
	<b>rockx </b>S
	<b>ezil.me</b>
	<b>wave</b>
	<b>shardpool.io</b>
	<b>valkyrie2</b>
	<b>huobi staking</b>
	<b>zilliqa2</b>
	<b>moonlet.io</b>
	<b>bountyblok</b>
	<b>everstake.one</b>
	<b>nodamatics.com</b>
	<b>zilpay</b>
	<b>avely finance</b>
	<b>viewblock</b>
	<b>atomicwallet</b>
	<b>binance staking</b>
	<b>luganodes</b>
	<b>cex.io</b>
	<b>blox-sdk staking</b>
	<b>valkyrie investments</b>
	<b>ignite dao</b>
	<b>zillet</b>
	<b>staked</b>
	<b>kucoin</b>
	<b>hashquark</b>
	<b>stakin</b>
		"""
	
	await bot.send_message(chat_id = message.from_user.id, text=msg, parse_mode='HTML', reply_markup=kb)

# @dp.message_handler()
# async def start(message: types.Message):
# 	user_id = message.from_user.id
# 	node_for_tracking = message.text
# 	await track_node(user_id, node_for_tracking)
	# while True:
	# 	if node_for_tracking == '/stop':
	# 		msg = 'Tracking stopped!'
	# 		await bot.send_message(user_id, msg)
	# 		break
	# 	await check_nodes(user_id, node_for_tracking)
	# node_for_tracking = ''

async def if_url_in_db(node_url, all_records_from_db):
	"""
	This function checks whether this node_url is in the database
	"""
	for elem in all_records_from_db:
		if node_url in elem:
			return True
	return False
	
async def track_node(user_id, node_for_tracking):
	responce = await get_nodes_info()

	for i in responce:
		node_url = i['node_url']
		name = i['name']
		current_dse_poch = i['current_dse_poch']
		current_mini_epoch = i['current_mini_epoch']
		if name.lower() == node_for_tracking.lower():
			all_records_from_db = await get_all_recors() # I get all the records from the database
			if await if_url_in_db(node_url, all_records_from_db):
				if current_dse_poch == 'error' or current_mini_epoch == 'error':
					msg = name + ':' + ' ' + 'something went wrong, check the node!'
					send_message = await bot.send_message(user_id, msg)
					uptime = False
					downtime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
					update_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

					await update(node_url, current_dse_poch, current_mini_epoch, uptime, downtime, update_time)
				else:
					msg = i['current_dse_poch'] + ' ' + i['current_mini_epoch']
					await bot.send_message(user_id, msg)
					uptime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
					downtime = False
					update_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
					await update(node_url, current_dse_poch, current_mini_epoch, uptime, downtime, update_time)
			else:
				if current_dse_poch == 'error' or current_mini_epoch == 'error':
					msg = name + ':' + ' ' + 'something went wrong, check the node!'
					send_message = await bot.send_message(user_id, msg)
					uptime = False
					downtime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
					update_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
					await write_to_db(node_url, name, current_dse_poch, current_mini_epoch, uptime, downtime, update_time)
				else:
					msg = i['current_dse_poch'] + ' ' + i['current_mini_epoch']
					await bot.send_message(user_id, msg)
					uptime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
					downtime = False
					update_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
					await write_to_db(node_url, name, current_dse_poch, current_mini_epoch, uptime, downtime, update_time)


async def track_nodes():
	while True:
		responce = await get_nodes_info()
		for i in responce:
			node_url = i['node_url']
			name = i['name']
			current_dse_poch = i['current_dse_poch']
			current_mini_epoch = i['current_mini_epoch']
			all_records_from_db = await get_all_recors() # I get all the records from the database
			if await if_url_in_db(node_url, all_records_from_db):
				if current_dse_poch == 'error' or current_mini_epoch == 'error':
					update_time = datetime.now().timestamp()
					recording_from_db = await get_recording_from_database(node_url)
					last_update_time = float(recording_from_db[-1])
					uptime = False
					last_downtime = float(recording_from_db[-2])
					downtime = update_time - last_update_time + last_downtime
					await update(node_url, current_dse_poch, current_mini_epoch, uptime, downtime, update_time)
				else:
					
					recording_from_db = await get_recording_from_database(node_url)
					last_update_time = float(recording_from_db[-1])
					downtime = False
					update_time = datetime.now().timestamp()
					last_uptime = float(recording_from_db[-3])
					uptime = update_time - last_update_time + last_uptime
					await update(node_url, current_dse_poch, current_mini_epoch, uptime, downtime, update_time)
			else:
				if current_dse_poch == 'error' or current_mini_epoch == 'error':
					last_upate_time = 0
					uptime = False
					downtime = 0
					last_downtime = 0
					update_time = datetime.now().timestamp()
					await write_to_db(node_url, name, current_dse_poch, current_mini_epoch, uptime, downtime, update_time)
				else:
					last_upate_time = 0
					downtime = False
					update_time = datetime.now().timestamp()
					uptime = 0
					last_uptime = 0
					await write_to_db(node_url, name, current_dse_poch, current_mini_epoch, uptime, downtime, update_time)


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.create_task(track_nodes())
	executor.start_polling(dp, skip_updates=True)