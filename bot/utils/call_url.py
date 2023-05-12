import asyncio
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
			async with session.post(node_url, data=params, headers=headers,) as response:
				async with session.post(node_url, data=params, headers=headers, timeout=2) as response:
					resp = await response.json()
					current_dse_poch = resp['result']['CurrentDSEpoch']
					current_mini_epoch = resp['result']['CurrentMiniEpoch']
					return {
						'node_url':node_url , 
						'name': name.lower(), 
						'current_ds_epoch': current_ds_epoch, 
						'current_mini_epoch': current_mini_epoch
					}
		except Exception as ex:
			current_dse_poch = None
			current_mini_epoch = None
			return {
				'node_url': node_url ,
				'name': name.lower(), 
				'current_ds_epoch': current_ds_epoch, 
				'current_mini_epoch': current_mini_epoch
			}


if __name__ == '__main__':
	asyncio.run(get_nodes_info())