from aiogram import types
from aiogram import Bot
import os 

bot = Bot(token=os.getenv('NODE_TOKEN'))

async def sending_warnings_to_users(chat_id, args):
	if args['current_ds_epoch'] == None:
		msg = f'Node "{args["node_name"]}" status is: {args["current_ds_epoch"]}! \n Check the operation of the node! (NONE)' 
		await bot.send_message(chat_id=chat_id, text=msg )
	else:
		if args['mini_epoch_diff']:
			msg = f'Node "{args["node_name"]}" is {args["mini_epoch_diff"]} blocks behind! \n Check the operation of the node!(MINI_E)'
			await bot.send_message(chat_id=chat_id, text=msg )
