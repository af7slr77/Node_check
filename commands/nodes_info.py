from aiogram import types
from db import async_session
from worker import Worker
from datetime import datetime


async def sent_nodes_info(call: types.CallbackQuery):
	node_name = call.data
	# print(node_name)
	node_data = Worker(async_session)
	node_data = await node_data._get_one_node_from_db(node_name)
	node = node_data[0]
	node_records =  node.records[-1]
	update_time = datetime.fromtimestamp(node_records.update_time)
	print(update_time)
	msg = f"{node.node_name}:\n" f"URL: {node.node_url}\n" f"Rating: {'100%'}\n" f"Current ds epoch: {node_records.current_ds_epoch}\n" f"Current mini epoch: {node_records.current_mini_epoch}\n" f"Last update: {update_time}\n"
	await call.message.answer(text=msg)