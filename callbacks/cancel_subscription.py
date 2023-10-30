from aiogram import types
from db.engine import get_async_session
from worker.worker_db import Worker
from .callbacks import CancelSubscriptionCallback


async def cancel_subscription(
	call: types.CallbackQuery, 
	callback_data: CancelSubscriptionCallback
	) -> None:
	async_session = await get_async_session()
	node_name: str = callback_data.node_name
	tg_user_id: int = call.from_user.id
	worker = Worker(async_session)
	result: bool = await worker._delete_user_from_user_nodes(
		node_name, 
		tg_user_id
	)
	if call.message:
		if result:
			unsubscribed_msg: str = f'You are unsubscribed from {node_name}!'
			await call.message.answer(text=unsubscribed_msg)
		else:
			node_not_found_msg: str = f'This node is not in your subscriptions!'
			await call.message.answer(text=node_not_found_msg)

