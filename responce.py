import requests
import asyncio
import aiohttp
import json
from datetime import datetime
from models import db, nodes,connection, write_to_db, get_all_recors, update, get_recording_from_database

async def get_nodes_urls(api_url):
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
					return {'node_url':node_url , 'name':name.lower(), 'current_dse_poch':current_dse_poch, 'current_mini_epoch':current_mini_epoch}
		except Exception as ex:
			current_dse_poch = 'error'
			current_mini_epoch = 'error'
			return {'node_url':node_url ,'name':name.lower(), 'current_dse_poch':current_dse_poch, 'current_mini_epoch':current_mini_epoch}


async def get_nodes_info():
	api_url = 'https://api.zilliqa.com/'
	urls = [{'node_url': 'https://stakingseed-api.seed.zilliqa.com', 'name': 'Zilliqa'}, {'node_url': 'https://api-zil.rockx.com/', 'name': 'RockX'}, {'node_url': 'https://zil-staking.ezil.me/api', 'name': 'Ezil.me'}, {'node_url': 'https://ssn.zilstream.com/api', 'name': 'Wave'}, {'node_url': 'https://seed-zil.shardpool.io', 'name': 'Shardpool.io'}, {'node_url': 'https://valkyrie2-api.seed.zilliqa.com', 'name': 'Valkyrie2'}, {'node_url': 'https://zilapi.2k7rqfvt5ahuc.hbpcrypto.com/api', 'name': 'Huobi Staking'}, {'node_url': 'https://stakingseed2-api.seed.zilliqa.com', 'name': 'Zilliqa2'}, {'node_url': 'https://ssn-zilliqa.moonlet.network/api', 'name': 'Moonlet.io'}, {'node_url': 'https://zilliqa.bountyblok.io/api', 'name': 'bountyblok'}, {'node_url': 'https://zilapi.everstake.one/status/TrdFrsHsHsYdOpfgNdTsIdxtJldtMfLd', 'name': 'Everstake.one'}, {'node_url': 'https://ssn1.api.zilliqa-mainnet.nodes.nodamatics.com', 'name': 'Nodamatics.com'}, {'node_url': 'https://ssn.zilpay.io/api', 'name': 'ZilPay'}, {'node_url': 'https://zilliqa.avely.fi/api', 'name': 'Avely Finance'}, {'node_url': 'https://ssn-api-mainnet.viewblock.io', 'name': 'ViewBlock'}, {'node_url': 'https://zilliqa.atomicwallet.io/api', 'name': 'AtomicWallet'}, {'node_url': 'https://api.binance-zilliqa.com', 'name': 'Binance Staking'}, {'node_url': 'https://zil-node.lgns.xyz/api', 'name': 'Luganodes'}, {'node_url': 'https://ssn-zilliqa.cex.io/api', 'name': 'CEX.IO'}, {'node_url': 'https://ssn.blox-sdk.com/api', 'name': 'BLOX-SDK Staking'}, {'node_url': 'https://api.v6e.technology/', 'name': 'Valkyrie Investments'}, {'node_url': 'https://ssn.ignitedao.io/api', 'name': 'Ignite DAO'}, {'node_url': 'https://ssn.zillet.io', 'name': 'Zillet'}, {'node_url': 'https://zilliqa-api.staked.cloud', 'name': 'Staked'}, {'node_url': 'https://staking-zil.kucoin.com/api', 'name': 'KuCoin'}, {'node_url': 'https://ssn-zilliqa.hashquark.io/api', 'name': 'HashQuark'}, {'node_url': 'https://ssn-zilliqa.stakin.com/api', 'name': 'Stakin'}]
	tasks = []
	for item in urls:
		node_url = item ['node_url']
		node_name = item ['name']
		tasks.append(asyncio.create_task(call_url(node_url, node_name, )))
		if len(tasks) == len(urls):
			result = await asyncio.gather(*tasks)
			tasks = []
			return result


async def if_url_in_db(node_url, all_records_from_db):
	"""
	This function checks whether this node_url is in the database
	"""
	for elem in all_records_from_db:
		if node_url in elem:
			return True
	return False


async def responce_processing():
	'''
	This function processes the response from the api and  calls "write_to_db" to write to db.
	'''
	responce = await get_nodes_info()
	print(responce)
	for i in responce:
		node_url = i['node_url']
		name = i['name']
		current_dse_poch = i['current_dse_poch']
		current_mini_epoch = i['current_mini_epoch']
		all_records_from_db = await get_all_recors() # I get all the records from the database
		if await if_url_in_db(node_url, all_records_from_db):
			if current_dse_poch == 'error' or current_mini_epoch == 'error':
				update_time = datetime.now().timestamp()
				recording_from_db = await get_recording_from_database(node_url)
				last_update_time = float(recording_from_db[-1])
				uptime = False
				last_downtime = float(recording_from_db[-2])
				downtime = update_time - last_update_time + last_downtime
				await update(node_url, current_dse_poch, current_mini_epoch, uptime, downtime, update_time)
			else:
						
				recording_from_db = await get_recording_from_database(node_url)
				last_update_time = float(recording_from_db[-1])
				downtime = False
				update_time = datetime.now().timestamp()
				last_uptime = float(recording_from_db[-3])
				uptime = update_time - last_update_time + last_uptime
				await update(node_url, current_dse_poch, current_mini_epoch, uptime, downtime, update_time)
		else:
			if current_dse_poch == 'error' or current_mini_epoch == 'error':
				last_upate_time = 0
				uptime = False
				downtime = 0
				last_downtime = 0
				update_time = datetime.now().timestamp()
				await write_to_db(node_url, name, current_dse_poch, current_mini_epoch, uptime, downtime, update_time)
			else:
				last_upate_time = 0
				downtime = False
				update_time = datetime.now().timestamp()
				uptime = 0
				last_uptime = 0
				await write_to_db(node_url, name, current_dse_poch, current_mini_epoch, uptime, downtime, update_time)


async def main():
	while True:
		await responce_processing()


if __name__ == '__main__':
	# loop = asyncio.get_event_loop()
	# loop.create_task(main())
	asyncio.run(main())
		# print(asyncio.run(get_nodes_info()))
