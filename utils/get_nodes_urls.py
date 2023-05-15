
from bot import MAX_NODE_TIMEOUT_SECOND, MAIN_NODE


async def get_nodes_urls():
	MAIN_NODE
	params = json.dumps( {
		"id": "1",
		"jsonrpc": "2.0",
		"method": "GetSmartContractSubState",
		"params": ["a7C67D49C82c7dc1B73D231640B2e4d0661D37c1", "ssnlist", []]
	} )
	headers = {"Content-Type": "application/json"}

	res = requests.post(api_url, data=params, headers=headers, timeout = MAX_NODE_TIMEOUT_SECOND).json()
	urls = []
	nodes_data = res['result']['ssnlist']
	for key in nodes_data:
		url = nodes_data[f'{key}']['arguments'][5]
		name = nodes_data[f'{key}']['arguments'][3]
		urls.append({'node_url':url, 'name':name})
		print(urls)
	return urls

if __name__ == '__main__':
	asyncio.run(get_nodes_info())
