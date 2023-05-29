import asyncio


class Worker():
	interval = 10000
	
	def __init__(self):
		pass

	async def run(self):
		try:
			nodes_info = await self._fetch_nodes()
			await self._update_db(nodes_info)
		except Exception as ex:
			print('run worker job error: ',  ex)
	
	async def _fetch_nodes(self):
		from utils import get_nodes_info, get_nodes_urls

		urls = await get_nodes_urls()
		nodes_info = await get_nodes_info(urls)
		return nodes_info

	async def _update_db(self, nodes_info):
		for node in nodes_info:
			if 'name' not in node:
				print('not found key in element: ', node)
				continue
if __name__ == '__main__':
	# asyncio.run(write())
	job = Worker()
	
	asyncio.run(job.run())