from aiogram import types

async def start(message: types.Message):
	msg = """
		 Hi! I am a bot for tracking the correct operation of Zilliqa nodes.
		Enter "/help <command>" to get help
	"""
	await message.answer(text="Hi!",)
	await message.answer(text="I am a bot for tracking the correct operation of Zilliqa nodes.",)
	await message.answer(text="Enter '/help <command>' to get help")
