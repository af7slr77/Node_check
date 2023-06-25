from aiogram import types
from db import async_session
from worker import Worker
from .subscribe_buttons import MyCallback

async def subscribe(call: types.CallbackQuery, callback_data: MyCallback):
	node_name = callback_data.node_name
	tg_user_id = call.from_user.id
	node_data_db = Worker(async_session)
	node_data_db = await node_data_db._subscribe(node_name, tg_user_id)
	print(node_data_db)
	# node_data = Worker(async_session)
	# node_data = await node_data._get_one_node_from_db(node_name)
	
	msg = f"You are subscribed to {node_name}!"
	await call.message.answer(text=msg)

    #попробовать передавать инфу через callback data