__all__ = ['register_user_comands', 'bot_commands']
from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.filters.command import Command
from commands.bot_commands import bot_commands
from commands.start import start
from commands.help import help_comand, help_func
from commands.nodes_buttons import get_nodes_buttons
from aiogram import F
from midelwares import RegisterCheck
from db import async_session
import asyncio
from .sent_nodes_info import sent_nodes_info
from .get_nodes_list import get_nodes_list
from .subscribe import subscribe
from .subscribe_buttons import MyCallback
from .sending_warnings_to_users import sending_warnings_to_users

async def register_user_comands(router: Router):
	# router.message.register(start, Command(commands=['start'])) - another variant
	router.message.register(start, CommandStart())
	router.message.register(help_comand, Command(commands=['help']))
	router.message.register(help_func, F.text == 'help')
	router.message.register(get_nodes_buttons, Command(commands=['get_nodes']))

	router.message.middleware(RegisterCheck())
	router.callback_query.middleware(RegisterCheck())

	router.callback_query.register(subscribe,  MyCallback.filter(F.action == 'subscribe'))
	# nodes keyboard's callbacks
	nodes_list = await get_nodes_list()
	for node in nodes_list:
		router.callback_query.register(sent_nodes_info, F.data == f'{node}')
		
	
	


# if __name__ == '__main__':
# 	register_user_comands(router=Router)
	