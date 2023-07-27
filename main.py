from aiogram import Dispatcher, Bot
import asyncio
import logging
import os
from commands import register_user_comands
from commands.bot_commands import bot_commands
from aiogram.types import BotCommand
from db.engine import async_session

async def bot():
	logging.basicConfig(level=logging.INFO)
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
	asyncio.run(bot())