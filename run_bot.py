from aiogram import Dispatcher, Bot
import asyncio
import logging
import os
from commands import register_user_comands
from commands.bot_commands import bot_commands
from aiogram.types import BotCommand
from db.engine import get_async_session
from logs.logs import init_bot_logger

init_bot_logger('bot')
blocks_logger = logging.getLogger('bot.run_bot')

async def bot():
	async_session = await get_async_session()
	#Gen commands menu
	comands_for_bot = []
	for cmd in bot_commands:
		comands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
	dp = Dispatcher()
	bot = Bot(token=os.getenv('NODE_TOKEN'))
	#Set commands
	await bot.set_my_commands(commands=comands_for_bot)
	await register_user_comands(dp)
	await dp.start_polling(bot, async_session=async_session)

if __name__ == '__main__':
	try:
		asyncio.run(bot())
	except Exception as ex:
		line = {
			'line':31
				}
		blocks_logger.warning(msg=ex, extra=line)