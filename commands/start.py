from aiogram import types

async def start(message: types.Message):
	msg = 'Hi! I am a bot for tracking nodes of Zilliqa. Enter "/help <command>" for help' 
	await message.answer(text=msg,)
