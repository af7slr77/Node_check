import asyncio


async def get_nodes_info(urls):
	tasks = []
	for item in urls:
		node_url = item['node_url']
		node_name = item['name']
		tasks.append(asyncio.create_task(call_url(node_url, node_name )))
		if len(tasks) == len(urls):
			result = await asyncio.gather(*tasks)
			tasks = []
			#return result  


if __name__ == '__main__':
	asyncio.run(get_nodes_info())