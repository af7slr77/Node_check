from aiogram import types
from aiogram.filters import CommandObject
from commands.bot_commands import bot_commands


async def help_comand(
	message: types.Message,
	command: CommandObject
	) -> None:
	if command.args:
		for cmd in bot_commands:
			if cmd[0] == command.args[0]:
				await message.answer(f"{cmd[0]} - {cmd[2]}")
		else:
			command_not_found_msg: str = "Command not found"
			await message.answer(text=command_not_found_msg)
	else:
		await help_func(message)
	
async def help_func(message:types.Message):
	msg: str = "To get a list of available nodes, select the command: /get_nodes <command>"
	await message.answer(text=msg)
