from aiogram import types
from aiogram.filters import CommandObject
from commands.bot_commands import bot_commands


async def help_comand(message: types.Message, command: CommandObject):
	print(command.args)
	if command.args:
		for cmd in bot_commands:
			print(cmd[0] == command.args)
			if cmd[0] == command.args:
				return await message.answer(text='')
		else:
			return await message.answer(text='Comand not found')
	else:
		return await message.answer('for help use /help')
