from worker.worker_db import Worker
from db import async_session
import asyncio

async def get_nodes_list():
    worker = Worker(async_session)
    data = await worker._fetch_nodes()
    new_nodes_list = []
    for node in data:
        node_name = node['node_name']
        new_nodes_list.append(node_name)
    return new_nodes_list
