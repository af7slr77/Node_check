from aiogram import types
from db import async_session
from worker.worker_db import Worker
from .callbacks import MyNodesCallback
from .callbacks import SubscribeCallback, CancelSubscriptionCallback, MyNodesCallback
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

async def my_nodes(call: types.CallbackQuery, callback_data: MyNodesCallback):
	node_name = callback_data.node_name
	tg_user_id = call.from_user.id
	worker = Worker(async_session)
	user = await worker._get_one_user_from_db(tg_user_id)
	users_nodes = user.users_nodes
	new_users_nodes = [users_nodes[i:i+2] for i in range(0, len(users_nodes), 2)]
	inline_kb = InlineKeyboardBuilder()
	for node in new_users_nodes:
		if len(node) == 1:
			inline_kb.row(InlineKeyboardButton(text=node[0].node_name, callback_data=f"{node[0].node_name}"))
		else:
			inline_kb.row(InlineKeyboardButton(text=node[0].node_name, callback_data=f"{node[0].node_name}"), InlineKeyboardButton(text=node[1].node_name, callback_data=f"{node[1].node_name}"))
	await call.message.answer(text='The nodes you are subscribed to:', reply_markup=inline_kb.as_markup())