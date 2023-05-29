import asyncio
import aiohttp
import json
from config.zilliqa import MAX_NODE_TIMEOUT_SECOND
from time import time

async def call_url(node_url, name):
	params = json.dumps( {
		"id": "1",
		"jsonrpc": "2.0",
		"method": "GetBlockchainInfo",
		"params": [""]
		} )
	headers = {"Content-Type": "application/json"}

	async with aiohttp.ClientSession(trust_env=True) as session:
		try:
			start_time = time()
			async with session.post(node_url, data=params, headers=headers, timeout=MAX_NODE_TIMEOUT_SECOND) as response:

				resp = await response.json()
				end_time = time()
				elapsed_time = end_time - start_time
				current_ds_epoch = resp['result']['CurrentDSEpoch']
				current_mini_epoch = resp['result']['CurrentMiniEpoch']
				return {
					'status': 200,
					'node_url':node_url , 
					'name': name.lower(), 
					'current_ds_epoch': current_ds_epoch, 
					'current_mini_epoch': current_mini_epoch,
					'elapsed_time': elapsed_time
				}
		except Exception as ex:
			current_ds_epoch = None
			current_mini_epoch = None
			return {
				'status': 408,
				'node_url': node_url ,
				'name': name.lower(), 
				'current_ds_epoch': current_ds_epoch, 
				'current_mini_epoch': current_mini_epoch,
				'elapsed_time': -1
			}

if __name__ == '__main__':
	asyncio.run(call_url('https://stakingseed-api.seed.zilliqa.com', 'zilliqa'))