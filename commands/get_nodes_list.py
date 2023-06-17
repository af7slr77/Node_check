from db import async_session
from worker import Worker
import asyncio
 
def get_nodes_list():
    nodes_list = Worker(async_session)
    nodes_list = asyncio.run(nodes_list._get_all_nodes_from_db())
    new_nodes_list = []
    for node in nodes_list:
        node_name = str(node[0].node_name)
        new_nodes_list.append(node_name)
    return new_nodes_list

nodes_list = get_nodes_list()