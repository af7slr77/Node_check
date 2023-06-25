from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

class MyCallback(CallbackData, prefix='my_callback'):
	node_name: str
	action: str

# subscribe_kb = InlineKeyboardBuilder()
# subscribe_kb.row(
# 	InlineKeyboardButton(text='Subscribe', callback_data=MyCallback.pack(node_name=node_name)),
# 	InlineKeyboardButton(text='Cancel subscription',  callback_data="cancel_subscription")
# )