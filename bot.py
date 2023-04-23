import asyncio
from config import token_bot, chat_id
from aiogram import Bot, Dispatcher, executor, types
from keyboard import kb
from main import get_nodes_info

bot = Bot(token=token_bot)
dp = Dispatcher(bot)


@dp.message_handler(commands=["help"])
async def help_comand(message: types.Message):
	msg = """
	Сhoose the notes to track:
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

@dp.message_handler()
async def start(message: types.Message):
	user_id = message.from_user.id
	node_for_tracking = message.text
	while True:
		await check_nodes(user_id, node_for_tracking)


async def check_nodes(user_id, node_for_tracking):
	responce = await get_nodes_info()
	for i in responce:
		if i['name'].lower() == node_for_tracking.lower():
			if i['current_dse_poch'] == 'error' or i['current_mini_epoch'] == 'error':
				msg = i['name']+':' + ' ' + 'something went wrong, check the node!'
				send_message = await bot.send_message(user_id, msg)
			else:
				msg = i['current_dse_poch'] + ' ' + i['current_mini_epoch']
				await bot.send_message(user_id, msg)
	

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.create_task(get_nodes_info())
	executor.start_polling(dp, skip_updates=True)