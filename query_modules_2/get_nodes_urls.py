import requests
import json
from config.zilliqa import MAIN_NODE, MAX_NODE_TIMEOUT_SECOND


def get_nodes_urls():
	params = json.dumps( {
		"id": "1",
		"jsonrpc": "2.0",
		"method": "GetSmartContractSubState",
		"params": ["a7C67D49C82c7dc1B73D231640B2e4d0661D37c1", "ssnlist", []]
	} )
	headers = {"Content-Type": "application/json"}

	result = requests.post(MAIN_NODE, data=params, headers=headers, timeout = MAX_NODE_TIMEOUT_SECOND).json()
	urls = []
	nodes_data = result['result']['ssnlist']
	for key in nodes_data:
		url = nodes_data[key]['arguments'][5]
		name = nodes_data[key]['arguments'][3]
		urls.append({'node_url':url, 'name':name.lower()})
	return urls

if __name__ == '__main__':
	get_nodes_urls()
