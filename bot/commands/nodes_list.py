from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types


commands=[
 	'zilliqa', 'rockx', 'ezil.me', 'wave', 'shardpool.io', 'valkyrie2', 'huobi staking', 'zilliqa2',
 	'moonlet.io', 'bountyblok', 'everstake.one', 'nodamatics.com', 'zilpay', 'avely finance', 'viewblock',
 	'atomicwallet', 'binance staking', 'luganodes', 'cex.io', 'blox-sdk staking', 'valkyrie investments',
 	'ignite dao', 'zillet', 'staked', 'kucoin', 'hashquark', 'stakin'
 	]

async def get_nodes_list(message:types.Message):
	nodes_markup = InlineKeyboardBuilder()
	for name in commands:
		nodes_markup.button(text=name, url='example.com')
	await message.answer(text='Select a node to get information:', reply_markup=nodes_markup.as_markup())