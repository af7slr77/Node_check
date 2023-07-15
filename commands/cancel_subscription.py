from aiogram import types
from db import async_session
from worker.worker_db import Worker
from .callbacks import CancelSubscriptionCallback

async def cancel_subscription(call: types.CallbackQuery, callback_data: CancelSubscriptionCallback):
	node_name = callback_data.node_name
	tg_user_id = call.from_user.id
	worker = Worker(async_session)
	await worker._delete_user_from_user_nodes(node_name, tg_user_id)
	# await call.message.answer(text=f'{tg_user_id}, {node_name}')
	# if await worker._check_subscribe(node_name, tg_user_id):
	# 	msg = f"You are already subscribed to {node_name}!"
	# 	await call.message.answer(text=msg)
	# else:
	# 	make_subscribe = await worker._subscribe(node_name, tg_user_id)
	# 	msg = f"You are subscribed to {node_name}!"
	# 	await call.message.answer(text=msg)