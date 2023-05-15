import asyncio
from get_nodes_urls import get_nodes_urls
from call_url import call_url

async def get_nodes_info(urls):
	tasks = [] 
	for item in urls:
		node_url = item['node_url']
		node_name = item['name']
		tasks.append(asyncio.create_task(call_url(node_url, node_name )))
		if len(tasks) == len(urls):
			result = await asyncio.gather(*tasks)
			tasks = []
			return result


if __name__ == '__main__':
	urls = asyncio.run(get_nodes_urls())
	asyncio.run(get_nodes_info(urls))