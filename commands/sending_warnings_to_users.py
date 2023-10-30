from aiogram import Bot
import os

bot_token: str = os.getenv("BOT_TOKEN")
bot = Bot(token=bot_token)


async def send_inactive_node_notifications(
	chat_id: int, 
	node_name: str
	) -> None:
	msg: str = f'Node "{node_name}" status is: Not active!\n Check the operation of the node!'
	await bot.send_message(
		chat_id=chat_id, 
		text=msg
	)

async def send_missed_blocks_notifications(
	chat_id: int, 
	node_name: str,  
	missed_blocks: int
	) -> None:
	msg: str = f'Node "{node_name}" is {missed_blocks} blocks behind!\n Check the operation of the node!'
	await bot.send_message(
		chat_id=chat_id, 
		text=msg
	)
