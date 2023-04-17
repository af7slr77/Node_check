import requests
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
		urls.append(url)
	return urls


def get_nodes_info(urls):
	params = json.dumps( {
		"id": "1",
		"jsonrpc": "2.0",
		"method": "GetBlockchainInfo",
		"params": [""]
	} )
	headers = {"Content-Type": "application/json"}
	res = requests.post(urls[1], data=params)
	return res

def  main():
	api_url = 'https://api.zilliqa.com/'
	print(get_nodes_info(get_nodes_urls(api_url)).json()['result'])

if __name__ == '__main__':
	main()