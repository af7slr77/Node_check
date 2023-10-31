import requests
import json
from config.zilliqa import MAIN_NODE, MAX_NODE_TIMEOUT_SECOND, URL_FOR_DELEGATES
from typing import List, Dict, Union

def get_nodes_urls() -> List[Dict[str, str| int]]:
	params: str = json.dumps(
		{
			"id": "1",
			"jsonrpc": "2.0",
			"method": "GetSmartContractSubState",
			"params": [
				"a7C67D49C82c7dc1B73D231640B2e4d0661D37c1", 
				"ssnlist", 
				[]
			]
		}
	)
	headers: Dict[str, str] = {"Content-Type": "application/json"}
	result: Dict = requests.post(
		MAIN_NODE, 
		data=params, 
		headers=headers, 
		timeout=MAX_NODE_TIMEOUT_SECOND
	).json()
	urls = []
	nodes_data = result['result']['ssnlist']
	for key in nodes_data:
		url: str = nodes_data[key]['arguments'][5]
		node_name: str = nodes_data[key]['arguments'][3]
		stake_amount: str = str(nodes_data[key]['arguments'][1])
		commission: str = str(nodes_data[key]['arguments'][7])
		reward: str = str(nodes_data[key]['arguments'][8])
		node_address = key
		urls.append(
			{
				'node_url': url,
				'node_name': node_name.lower(), 
				'stake_amount': stake_amount,
				'commission': commission,
				'node_address': node_address
			}
		)
	return urls

def get_delegators() -> Dict[str, int]:
	params: str = json.dumps(
		{
			"id": '1',
			"jsonrpc": "2.0",
			"method": "GetSmartContractSubState",
			"params": [
				"a7c67d49c82c7dc1b73d231640b2e4d0661d37c1",
				"ssn_deleg_amt",
				[]
			]
		}
	)
	resp = requests.post(URL_FOR_DELEGATES, data=params).json()
	responce = resp['result']['ssn_deleg_amt']
	with open('responce.json', 'w', encoding='utf-8') as file:
		json.dump(responce, file)
		file.write('\n')
	with open('responce.json') as f:
		data = json.load(f)
	number_of_delegates = {}
	for key, value in data.items():
		number_of_delegates[f"{key}"] = len(value)
	return number_of_delegates

def get_total_info() -> List[Dict[str, str|int]]:
	delegators = get_delegators()
	nodes = get_nodes_urls()
	for node in nodes:
		node_address = node['node_address']
		number_of_delegates = delegators.get(f"{node_address}", 0)
		node['number_of_delegates'] = number_of_delegates
	return nodes
