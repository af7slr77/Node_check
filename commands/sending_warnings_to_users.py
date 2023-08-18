from aiogram import types
from aiogram import Bot
import os 

bot = Bot(token=os.getenv('NODE_TOKEN'))

async def send_inactive_node_notifications(chat_id, node_name):
	msg = f'Node "{node_name}" status is: Not active! \n Check the operation of the node!' 
	await bot.send_message(chat_id=chat_id, text=msg )

async def send_missed_blocks_notifications(chat_id, node_name,  missed_blocks):
	msg = f'Node "{node_name}" is {missed_blocks} blocks behind! \n Check the operation of the node!'
	await bot.send_message(chat_id=chat_id, text=msg )