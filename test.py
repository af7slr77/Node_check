from aiogram import Dispatcher, Bot
import asyncio
import logging
import os
from commands import register_user_comands
from commands.bot_commands import bot_commands
from aiogram.types import BotCommand
from db import async_session
from midelwares import RegisterCheck
from aiogram import BaseMiddleware
from worker.worker_db import Worker
import threading
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



# def run_bot():
# 	loop = asyncio.new_event_loop()
# 	asyncio.run(bot())

# # Создаем класс для сообщений
# class Message:
# 	def __init__(self, content):
# 		self.content = content

# Функция, выполняемая в первом потоке
async def thread1_func():
	# 
	
	# await bot()
	pass
	# while True:
	# 	# Ваш асинхронный код для выполнения в первом потоке
	# 	# В данном примере просто отправляем сообщение во второй поток
	# 	message = Message("Hello from Thread 1")
	# 	await thread2.receive_message(message)
	# 	await asyncio.sleep(1)  # Ждем 1 секунду

# Функция, выполняемая во втором потоке
async def thread2_func():
	# while True:
	engine = create_async_engine('sqlite+aiosqlite:///database.db')
	async_session = async_sessionmaker(engine)
	worker = Worker(async_session)
	await worker.run()
	# pass
		# message = await thread2.get_message()
		# print(f"Received message in Thread 2: {message.content}")
		# await asyncio.sleep(1)  # Ждем 1 секунду

# Создаем класс для второго потока, который будет иметь методы для отправки и получения сообщений
# class Thread2:
# 	def __init__(self):
# 		self.message = None
# 		self.event = asyncio.Event()

# 	async def receive_message(self, message):
# 		self.message = message
# 		self.event.set()  # Устанавливаем событие, чтобы разбудить поток

# 	async def get_message(self):
# 		await self.event.wait()  # Ожидаем события от первого потока
# 		message = self.message
# 		self.event.clear()  # Сбрасываем событие
# 		return message
async def main():
	await asyncio.gather(thread1_func(), thread2_func())

if __name__ == '__main__':

	# Создаем экземпляр второго потока
	# thread2 = Thread2()

	# Запускаем асинхронные задачи
	
	loop = asyncio.new_event_loop()
	# asyncio.set_event_loop(loop)
	loop.run_until_complete(main())
		