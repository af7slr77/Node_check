from aiogram import types
from db.engine import get_async_session
from worker.worker_db import Worker
from .callbacks import CancelSubscriptionCallback

async def cancel_subscription(call: types.CallbackQuery, callback_data: CancelSubscriptionCallback):
	async_session = await get_async_session()
	node_name = callback_data.node_name
	tg_user_id = call.from_user.id
	worker = Worker(async_session)
	await worker._delete_user_from_user_nodes(node_name, tg_user_id)
	msg = f'You are unsubscribed from {node_name}!'
	await call.message.answer(text=msg)
