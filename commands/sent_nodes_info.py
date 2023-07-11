from aiogram import types
from db import async_session
from worker.worker_db import Worker
from datetime import datetime
from .subscribe_buttons import MyCallback
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


async def sent_nodes_info(call: types.CallbackQuery):
	node_name = call.data
	node_data = Worker(async_session)
	node = await node_data._get_one_node_from_db(node_name)
	node_records =  node.records[-1]
	update_time = datetime.fromtimestamp(node_records.update_time)
	subscribe_kb = InlineKeyboardBuilder()
	subscribe_kb.row(
		InlineKeyboardButton(text='Subscribe', callback_data = MyCallback(node_name= node_name, action= 'subscribe').pack()),
		InlineKeyboardButton(text='Cancel subscription',  callback_data="cancel_subscription"))


	msg = f"{node.node_name}:\n" f"URL: {node.node_url}\n" f"Rating: {'100%'}\n" f"Current ds epoch: {node_records.current_ds_epoch}\n" f"Current mini epoch: {node_records.current_mini_epoch}\n" f"Last update: {update_time}\n"
	await call.message.answer(text=msg, reply_markup=subscribe_kb.as_markup())