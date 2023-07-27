from aiogram import types
from db.engine import async_session
from worker.worker_db import Worker
from datetime import datetime
from .callbacks import SubscribeCallback, CancelSubscriptionCallback, MyNodesCallback
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


async def sent_nodes_info(call: types.CallbackQuery):
	node_name = call.data
	node_data = Worker(async_session)
	node = await node_data._get_one_node_from_db(node_name)
	node_records =  node.records[-1]
	fromtimestamp = datetime.fromtimestamp(node_records.update_time)
	update_time = fromtimestamp.strftime('%d-%m-%Y %H:%M:%S')
	subscribe_kb = InlineKeyboardBuilder()
	subscribe_kb.row(
		InlineKeyboardButton(text='Subscribe', callback_data = SubscribeCallback(node_name=node_name, action='subscribe').pack()),
		InlineKeyboardButton(text='Cancel Subscription',  callback_data=CancelSubscriptionCallback(node_name= node_name, action='cancel_subscription').pack()))
	subscribe_kb.row(InlineKeyboardButton(text='My nodes',  callback_data=MyNodesCallback(node_name=node_name, action='my_nodes').pack()))
	msg = f"{node.node_name}:\n" "\n" f"URL:  {node.node_url}\n" "\n" f"Rating:  {node_records.rating}%\n" "\n" f"Current ds epoch:  {node_records.current_ds_epoch}\n" "\n" f"Current mini epoch:  {node_records.current_mini_epoch}\n" "\n" f"Last update:  {update_time}\n"
	await call.message.answer(text=msg, reply_markup=subscribe_kb.as_markup())