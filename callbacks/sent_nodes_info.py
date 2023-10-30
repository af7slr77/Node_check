from aiogram import types
from db.engine import get_async_session
from worker.worker_db import Worker
from .callbacks import SubscribeCallback
from .callbacks import CancelSubscriptionCallback
from .callbacks import MyNodesCallback
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardButton
from time import time
from typing import Tuple, Union

async def check_current_ds_and_min_epoch(
	current_mini_epoch: Union[int, None], 
	current_ds_epoch: Union[int, None]
) -> Tuple[Union[int, None], Union[int, None]]:
	if current_mini_epoch is not None and current_ds_epoch is not None:
		current_mini_epoch = int("{:,.0f}".format(
			round(current_mini_epoch))
		)
		current_ds_epoch = int("{:,.0f}".format(
			round(current_ds_epoch))
		)
		return current_mini_epoch, current_ds_epoch
	else:
		return None, None
		
async def sent_nodes_info(call: types.CallbackQuery):
	async_session = await get_async_session()
	node_name = call.data
	if node_name is not None:
		node_data = Worker(async_session)
		node = await node_data._get_one_node_from_db(node_name)
		node_records =  node.records[-1]
		last_update = "{:,.0f}".format(
			int(time() - node_records.update_time)/ 10 ** 3
		) 
		stake_amount = "{:,.2f}".format(
			int(node_records.stake_amount) / 10 ** 12
		)
		commission = "{:,.1f}".format(
			int(node_records.commission) / 10 ** 7
		) 
		number_of_delegates = "{:,.0f}".format(
			round(int(node_records.number_of_delegates))
		)
		checked_blocks = await check_current_ds_and_min_epoch(
			node_records.current_mini_epoch, 
			node_records.current_ds_epoch
		)
		current_mini_epoch = checked_blocks[0]
		current_ds_epoch = checked_blocks[1]
		subscribe_kb = InlineKeyboardBuilder()
		subscribe_kb.row(
			InlineKeyboardButton(
				text='Subscribe', 
				callback_data = SubscribeCallback(
					node_name=node_name, 
					action='subscribe'
				).pack()
			),
			InlineKeyboardButton(
				text='Cancel Subscription',  
				callback_data=CancelSubscriptionCallback(
					node_name= node_name, 
					action='cancel_subscription'
				).pack())
		)
		subscribe_kb.row(
			InlineKeyboardButton(
				text='My nodes',  
				callback_data=MyNodesCallback(
					node_name=node_name, 
					action='my_nodes'
				).pack()
			)
		)
		if call.message:
			msg = f"""
				Node: {node.node_name}\n
				URL: {node.node_url}\n
				Rating: {node_records.rating}%\n
				Stake amount: {stake_amount}\n
				Commission: {commission}%\n
				Delegates: {number_of_delegates}\n
				Current ds epoch: {current_ds_epoch}\n
				Current mini epoch: {current_mini_epoch}\n
				Last update: {last_update} seconds ago.
				"""
			await call.message.answer(
				text=msg, 
				reply_markup=subscribe_kb.as_markup()
			)
