__all__ = ['register_user_comands', 'bot_commands']
from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.filters.command import Command
from commands.start import start
from commands.help import help_comand, help_func
from commands.nodes_buttons import get_nodes_buttons
from aiogram import F
from midelwares import RegisterCheck
from callbacks.sent_nodes_info import sent_nodes_info
from .get_nodes_list import get_nodes_list
from callbacks.subscribe import subscribe
from callbacks.cancel_subscription import cancel_subscription
from callbacks.my_nodes import get_my_nodes_list
from callbacks.callbacks import SubscribeCallback
from callbacks.callbacks import CancelSubscriptionCallback
from callbacks.callbacks import MyNodesCallback


async def register_user_comands(router: Router):
	router.message.register(start, CommandStart())
	router.message.register(help_comand, Command(commands=['help']))
	router.message.register(help_func, F.text == 'help')
	router.message.register(
		get_nodes_buttons, 
		Command(commands=['get_nodes'])
	)
	router.message.middleware(RegisterCheck())
	router.callback_query.middleware(RegisterCheck())
	router.callback_query.register(
		subscribe,  
		SubscribeCallback.filter(F.action == 'subscribe')
	)
	router.callback_query.register(
		cancel_subscription,  
		CancelSubscriptionCallback.filter(
			F.action == 'cancel_subscription'
			)
		)
	router.callback_query.register(
		get_my_nodes_list,  
		MyNodesCallback.filter(F.action == 'my_nodes')
	)
	nodes_list = await get_nodes_list()
	for node in nodes_list:
		router.callback_query.register(
			sent_nodes_info, 
			F.data == f'{node}'
		)
