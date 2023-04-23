import requests
import asyncio
import aiohttp
import json



def get_nodes_urls(api_url):
	params = json.dumps( {
		"id": "1",
		"jsonrpc": "2.0",
		"method": "GetSmartContractSubState",
		"params": ["a7C67D49C82c7dc1B73D231640B2e4d0661D37c1", "ssnlist", []]
	} )
	headers = {"Content-Type": "application/json"}

	res = requests.post(api_url, data=params, headers=headers ).json()
	urls = []
	nodes_data = res['result']['ssnlist']
	for key in nodes_data:
		url = nodes_data[f'{key}']['arguments'][5]
		name = nodes_data[f'{key}']['arguments'][3]
		urls.append({'node_url':url, 'name':name})
	return urls

async def call_url(url, name):
	params = json.dumps( {
		"id": "1",
		"jsonrpc": "2.0",
		"method": "GetBlockchainInfo",
		"params": [""]
	} )
	headers = {"Content-Type": "application/json"}

	async with aiohttp.ClientSession(trust_env=True) as session:
		try:
			async with session.post(url, data=params, headers=headers,) as response:
				async with session.post(url, data=params, headers=headers, timeout=3) as response:
					resp = await response.json()
					current_dse_poch = resp['result']['CurrentDSEpoch']
					current_mini_epoch = resp['result']['CurrentMiniEpoch']
					return {'name':name.lower(), 'current_dse_poch':current_dse_poch, 'current_mini_epoch':current_mini_epoch}
		except Exception as ex:
			current_dse_poch = 'error'
			current_mini_epoch = 'error'
			return {'name':name.lower(), 'current_dse_poch':current_dse_poch, 'current_mini_epoch':current_mini_epoch}

async def get_nodes_info():
	api_url = 'https://api.zilliqa.com/'
	urls = get_nodes_urls(api_url)
	# urls = [{'node_url': 'https://ssn.zilpay.io/api', 'name': 'ZilPay'}]
	# while True:
	tasks = []
	for item in urls:
		node_url = item ['node_url']
		node_name = item ['name']
		tasks.append(asyncio.create_task(call_url(node_url, node_name)))
		if len(tasks) == len(urls):
			result = await asyncio.gather(*tasks)
			tasks = []
			return result



# if __name__ == '__main__':
# 	loop = asyncio.get_event_loop()
# 	loop.run_until_complete(main())
