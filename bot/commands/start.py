from aiogram import types


async def start(message: types.Message):
	msg = 'Hi! I am a bot for tracking nodes of Zilliqa. Press "/help" for help' 
	await message.answer(text=msg,)
