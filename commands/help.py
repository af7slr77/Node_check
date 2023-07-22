from aiogram import types
from aiogram.filters import CommandObject
from commands.bot_commands import bot_commands


async def help_comand(message: types.Message, command: CommandObject):
	if command.args:
		for cmd in bot_commands:
			if cmd[0] == command.args:
				return await message.answer(f"{cmd[0]} - {cmd[1]}")
		else:
			return await message.answer(text='Comand not found')
	else:
		return await help_func(message)

async def help_func(message:types.Message):
	return await message.answer('For help use /help <command>')
