import requests
import json
from config.zilliqa import MAX_NODE_TIMEOUT_SECOND
from time import time
import logging
from logs.logs import init_worker_logger 
from typing import Dict, Union

init_worker_logger('request_modules')
logger = logging.getLogger('request_modules.call_url')
 

def call_url(node_url: str) -> Dict[str, Union[int, None, float]]:
	params: str = json.dumps(
		{
			"id": "1",
			"jsonrpc": "2.0",
			"method": "GetBlockchainInfo",
			"params": [""]
		} 
	)
	headers = {"Content-Type": "application/json"}
	proxies = {''}
	try:
		start_time: float = time()
		resp = requests.post(
			node_url, 
			data=params, 
			headers=headers, 
			timeout = MAX_NODE_TIMEOUT_SECOND
		).json()
		end_time: float = time()
		response_time: float = end_time - start_time
		current_ds_epoch: int = int(resp['result']['CurrentDSEpoch'])
		current_mini_epoch: int = int(resp['result']['CurrentMiniEpoch'])
		if response_time < MAX_NODE_TIMEOUT_SECOND:
			return {
				'status': 200,
				'current_ds_epoch': current_ds_epoch, 
				'current_mini_epoch': current_mini_epoch,
				'response_time': response_time,
			}

	except Exception as ex:
		logger.warning(msg=ex, extra={'line':44})
		return {
			'status': 408,
			'current_ds_epoch': None, 
			'current_mini_epoch': None,
			'response_time': None,
		}
	return {
		'status': 500,
		'current_ds_epoch': None, 
		'current_mini_epoch': None,
		'response_time': None,
	}