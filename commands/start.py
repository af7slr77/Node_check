from aiogram import types


async def start(message: types.Message):
	await message.answer(text="Hi!",)
	await message.answer(text="I am a bot for tracking the correct operation of Zilliqa nodes.",)
	await message.answer(text="Enter '/help <command>' to get help")
