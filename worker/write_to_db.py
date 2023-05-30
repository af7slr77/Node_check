import asyncio
from lib.get_nodes_info import get_nodes_info
from lib.get_nodes_urls import get_nodes_urls
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import Node, Records
from datetime import datetime

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
		urls = get_nodes_urls()
		
		nodes_info = await get_nodes_info(urls)
		return nodes_info

	async def _update_db(self, nodes_info):
		engine = create_async_engine('sqlite+aiosqlite:///database.db')
		async_session = async_sessionmaker(engine)
		async with async_session() as session:
			for node in nodes_info:
				# print(node['name'])
				try:
					new_node = Node(
						node_url = node['node_url'],
						node_name = node['name'],
					)
					new_record = Records(
						score = 'score',
						update_time = datetime.utcnow().timestamp()
					)
					new_node.records.append(new_record)
					session.add(new_node)
					session.add(new_record)
					await session.commit()
				except Exception as ex:
					print(ex)

				
		
		# session.add(new_node)
		# session.commit()

		

if __name__ == '__main__':
	# asyncio.run(write())
	job = Worker()
	
	asyncio.run(job.run())