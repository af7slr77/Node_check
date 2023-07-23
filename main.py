from aiogram import Dispatcher, Bot
import asyncio
import logging
import os
from commands import register_user_comands
from commands.bot_commands import bot_commands
from aiogram.types import BotCommand
# from db import async_session
from midelwares import RegisterCheck
from aiogram import BaseMiddleware
from worker.worker_db import Worker
from block_worker.blocks_db import BlocksWorker
import threading
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

async def bot():
	engine = create_async_engine('sqlite+aiosqlite:///database.db')
	async_session = async_sessionmaker(engine)
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

async def thread1_func():
	await bot()
	# pass

async def thread2_func():
	pass
	# while True:
	# engine = create_async_engine('sqlite+aiosqlite:///database.db')
	# async_session = async_sessionmaker(engine)
	# worker = Worker(async_session)
	# await worker.run()

async def main():
	await asyncio.gather(thread1_func(), thread2_func())

if __name__ == '__main__':
	loop = asyncio.new_event_loop()
	loop.run_until_complete(main())