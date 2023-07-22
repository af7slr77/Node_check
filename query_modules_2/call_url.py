import requests
import json
from config.zilliqa import MAX_NODE_TIMEOUT_SECOND
from time import time

def call_url(node_url, name):
	params = json.dumps( {
		"id": "1",
		"jsonrpc": "2.0",
		"method": "GetBlockchainInfo",
		"params": [""]
		} )
	headers = {"Content-Type": "application/json"}
	proxies = {
    # 'http': '207.246.86.43:6802',
    'http': 'socks4://169.239.223.136:52178'
}

	try:
		start_time = time()
		
		resp = requests.post(node_url, data=params, headers=headers, timeout = MAX_NODE_TIMEOUT_SECOND, proxies=proxies).json()
		end_time = time()
		response_time = end_time - start_time
		current_ds_epoch = int(resp['result']['CurrentDSEpoch'])
		current_mini_epoch = int(resp['result']['CurrentMiniEpoch'])
		return {
			'status': 200,
			'node_url':node_url , 
			'node_name': name.lower(), 
			'current_ds_epoch': current_ds_epoch, 
			'current_mini_epoch': current_mini_epoch,
			'response_time': response_time
		}
	except Exception as ex:
		print(ex)
		current_ds_epoch = None
		current_mini_epoch = None
		return {
			'status': 408,
			'node_url': node_url,
			'node_name': name.lower(), 
			'current_ds_epoch': current_ds_epoch, 
			'current_mini_epoch': current_mini_epoch,
			'response_time': 0
		}

if __name__ == '__main__':
	print(call_url('https://stakingseed-api.seed.zilliqa.com', 'zilliqa'))