from aiogram import types
from db.engine import async_session
from worker.worker_db import Worker
from .callbacks import SubscribeCallback

async def subscribe(call: types.CallbackQuery, callback_data: SubscribeCallback):
	node_name = callback_data.node_name
	tg_user_id = call.from_user.id
	worker = Worker(async_session)
	if await worker._check_subscribe(node_name, tg_user_id):
		msg = f"You are already subscribed to {node_name}!"
		await call.message.answer(text=msg)
	else:
		make_subscribe = await worker._subscribe(node_name, tg_user_id)
		msg = f"You are subscribed to {node_name}!"
		await call.message.answer(text=msg)
