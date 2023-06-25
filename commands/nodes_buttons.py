from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from lib.get_nodes_urls import get_nodes_urls
from .get_nodes_list import get_nodes_list


buttons = get_nodes_list()

async def get_nodes_buttons(message:types.Message):
	# buttons = get_nodes_urls()
	res = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
	inline_kb = InlineKeyboardBuilder()
	for i in res:
		# print(i[0]['name'])
		# print(i)
		if len(i) == 1:
			inline_kb.row(InlineKeyboardButton(text=i[0], callback_data=f"{i[0]}"))
		else:
			inline_kb.row(InlineKeyboardButton(text=i[0], callback_data=f"{i[0]}"), InlineKeyboardButton(text=i[1], callback_data=f"{i[1]}"))
	await message.answer(text='Select a node to get information:', reply_markup=inline_kb.as_markup())



if __name__ == '__main__':
	pass