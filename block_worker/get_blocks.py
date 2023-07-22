import requests
import json
from config.zilliqa import MAIN_NODE, MAX_NODE_TIMEOUT_SECOND


def get_blocks():
	params = json.dumps( {
		"id": "1",
		"jsonrpc": "2.0",
		"method": "GetBlockchainInfo",
		"params": [""]
	} )
	headers = {"Content-Type": "application/json"}

	result = requests.post(MAIN_NODE, data=params, headers=headers, timeout = MAX_NODE_TIMEOUT_SECOND).json()
	# urls = []
	current_ds_epoch = result['result']['CurrentDSEpoch']
	current_mini_epoch = result['result']['CurrentMiniEpoch']
	blocks = {
		'current_ds_epoch': current_ds_epoch,
		'current_mini_epoch': current_mini_epoch
	}
	return blocks

if __name__ == '__main__':
	get_nodes_urls()
