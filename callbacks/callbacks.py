from aiogram.filters.callback_data import CallbackData


class SubscribeCallback(CallbackData, prefix='subscribe_callback'):
	node_name: str
	action: str

class CancelSubscriptionCallback(CallbackData, prefix='cancel_subscription'):
	node_name: str
	action: str

class MyNodesCallback(CallbackData, prefix='my_nodes'):
	node_name: str
	action: str
