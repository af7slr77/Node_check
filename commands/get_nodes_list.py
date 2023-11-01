from worker.worker_db import Worker
from db.engine import get_async_session
from typing import List, Tuple
from models.models import Node

async def get_nodes_list() -> List[str]:
	async_session = await get_async_session()
	worker = Worker(async_session)
	data: List[Node] = await worker._buttons()
	new_nodes_list: List = []
	for node in data:
		node_name: str = node[0].node_name
		new_nodes_list.append(node_name)
	return new_nodes_list
