from aiogram import types
from db.engine import get_async_session
from worker.worker_db import Worker
from .callbacks import MyNodesCallback
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardButton


async def sort_users_nodes(users_nodes: list) -> list:
	sorted_users_nodes: list = [
		users_nodes[i:i+2] 
		for i in range(0, len(users_nodes), 2)]
	return sorted_users_nodes

async def get_my_nodes_list(
	call: types.CallbackQuery,
	callback_data:MyNodesCallback
	) -> None:
	async_session = await get_async_session()
	node_name = callback_data.node_name
	tg_user_id = call.from_user.id
	worker = Worker(async_session)
	user = await worker._get_one_user_from_db(tg_user_id)
	if user is not None:
		users_nodes = user.users_nodes
		if call.message:
			if users_nodes == []:
				await call.message.answer(
					text='You are not subscribed to any node!'
				)
				await call.message.answer(
					text='To get a list of available nodes, select the command: /get_nodes <command>'
				)
			else:
				sorted_users_nodes = await sort_users_nodes(users_nodes)
				inline_kb = InlineKeyboardBuilder()
				for node in sorted_users_nodes:
					if len(node) == 1:
						inline_kb.row(
							InlineKeyboardButton(
								text=node[0].node_name, 
								callback_data=f"{node[0].node_name}"
								)
							)
					else:
						inline_kb.row(
							InlineKeyboardButton(
								text=node[0].node_name, 
								callback_data=f"{node[0].node_name}"
								), 
							InlineKeyboardButton(
								text=node[1].node_name, 
								callback_data=f"{node[1].node_name}"
								)
						)
				await call.message.answer(
					text='The nodes you are subscribed to:', 
					reply_markup=inline_kb.as_markup()
				)
