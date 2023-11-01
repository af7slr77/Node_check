from aiogram import types
from db.engine import get_async_session
from worker.worker_db import Worker
from .callbacks import SubscribeCallback


async def subscribe(
	call: types.CallbackQuery, 
	callback_data: SubscribeCallback
	) -> None:
	async_session = await get_async_session()
	node_name: str = callback_data.node_name
	tg_user_id: int = call.from_user.id
	worker = Worker(async_session)
	if call.message:
		if await worker._check_subscribe(node_name, tg_user_id):
			subscribed_msg: str = f"You are already subscribed to {node_name}!"
			await call.message.answer(text=subscribed_msg)
		else:
			await worker._subscribe(
				node_name, 
				tg_user_id
			)
			already_subscribed_msg: str = f"You are subscribed to {node_name}!"
			await call.message.answer(text=already_subscribed_msg)
