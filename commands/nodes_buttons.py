from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton
from aiogram import types
from utils.get_nodes_urls import get_nodes_urls


# buttons=[
#  	'zilliqa', 'rockx', 'ezil.me', 'wave', 'shardpool.io', 'valkyrie2', 'huobi staking', 'zilliqa2',
#  	'moonlet.io', 'bountyblok', 'everstake.one', 'nodamatics.com', 'zilpay', 'avely finance', 'viewblock',
#  	'atomicwallet', 'binance staking', 'luganodes', 'cex.io', 'blox-sdk staking', 'valkyrie investments',
#  	'ignite dao', 'zillet', 'staked', 'kucoin', 'hashquark', 'stakin'
#  	]

# async def get_nodes_list(message:types.Message):
# 	buttons = await get_nodes_urls()
# 	res = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
# 	inline_kb = InlineKeyboardBuilder()
# 	for i in res:
# 		print(i[0]['node_url'])
# 		if len(i) == 1:
# 			inline_kb.row(InlineKeyboardButton(text=i[0]['name'], url=i[0]['node_url']))
# 		else:
# 			inline_kb.row(InlineKeyboardButton(text=i[0]['name'], url=i[0]['node_url']), InlineKeyboardButton(text=i[1]['name'], url=i[1]['node_url']))
# 	await message.answer(text='Select a node to get information:', reply_markup=inline_kb.as_markup())



if __name__ == '__main__':
	pass