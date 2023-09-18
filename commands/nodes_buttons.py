from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardButton
from aiogram import types
from .get_nodes_list import get_nodes_list

async def get_sorted_nodes_list():
	nodes_list = await get_nodes_list()
	sorted_nodes_list = [
		nodes_list[elem:elem+2] 
		for elem in range(0, len(nodes_list), 2)]
	return sorted_nodes_list

async def get_nodes_buttons(message:types.Message):
	sorted_nodes_list = await get_sorted_nodes_list()
	inline_kb = InlineKeyboardBuilder()
	for nodes in sorted_nodes_list:
		if len(nodes) == 1:
			inline_kb.row(
				InlineKeyboardButton(
					text=nodes[0], 
					callback_data=f"{nodes[0]}"
				)
			)
		else:
			inline_kb.row(
				InlineKeyboardButton(
					text=nodes[0], 
					callback_data=f"{nodes[0]}"
				), 
				InlineKeyboardButton(
					text=nodes[1], 
					callback_data=f"{nodes[1]}"
				)
			)
	msg = 'Select a node to get information:'
	await message.answer(
		text=msg, 
		reply_markup=inline_kb.as_markup()
	)
