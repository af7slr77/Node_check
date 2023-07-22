from .call_url import call_url
from time import sleep, time

def get_nodes_info(urls):
	result = []
	for item in urls:
		node_url = item['node_url']
		node_name = item['name']
		resp = call_url(node_url, node_name)
		result.append(resp)
		sleep(2)
	return result


if __name__ == '__main__':
	from .get_nodes_urls import get_nodes_urls
	start_time = time()
	print(get_nodes_info(get_nodes_urls()))
	end_time = time()
	response_time = end_time - start_time
	print(response_time)
	