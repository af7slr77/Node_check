import requests
import json
from config.zilliqa import MAIN_NODE, MAX_NODE_TIMEOUT_SECOND
from time import time

def get_blocks():
	params = json.dumps( {
		"id": "1",
		"jsonrpc": "2.0",
		"method": "GetBlockchainInfo",
		"params": [""]
	} )
	headers = {"Content-Type": "application/json"}
	try:
		start = time()
		result = requests.post(MAIN_NODE, data=params, headers=headers, timeout = MAX_NODE_TIMEOUT_SECOND).json()
		stop = time()
		responce_time = stop - start
		current_ds_epoch = result['result']['CurrentDSEpoch']
		current_mini_epoch = result['result']['CurrentMiniEpoch']
		blocks = {
			'current_ds_epoch': current_ds_epoch,
			'current_mini_epoch': current_mini_epoch,
			'response_time': responce_time
		}
		return blocks
	except Exception:
		blocks = {
			'current_ds_epoch': None,
			'current_mini_epoch': None,
			'response_time': None
		}
		return blocks

if __name__ == '__main__':
	print(get_blocks())
