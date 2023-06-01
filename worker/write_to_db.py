import asyncio
from lib.get_nodes_info import get_nodes_info
from lib.get_nodes_urls import get_nodes_urls
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import Node, Records
from datetime import datetime
from sqlalchemy import select

class Worker():
	interval = 10000
	_async_session = None

	def __init__(self, async_session):
		self._async_session = async_session

	async def run(self):
		try:
			nodes_info = await self._fetch_nodes()
			await self._update_db(nodes_info)
			# await self._get_all_records_db()
			
		except Exception as ex:
			print('run worker job error: ',  ex)
	
	async def _fetch_nodes(self):
		urls = get_nodes_urls()
		nodes_info = await get_nodes_info(urls)
		return nodes_info

	async def _get_all_records_db(self):
		async with self._async_session() as session:
			all_nodes = await session.execute(select(Node))
			node = await session.execute(select(Node).filter_by(node_name = 'zilpay'))
			print(dir(node))
			# for i in all_nodes:
			# 	print(i[0].nodes_id)

	async def _update_db(self, nodes_info):
		async with self._async_session() as session:
			for node in nodes_info:
				if await session.execute(select(Node).filter_by(node_name = node['node_name'])):
					print(True)
					try:
						new_node = Node(
						)
						new_record = Records(
							score = 'score',
							update_time = datetime.utcnow().timestamp(),
							current_ds_epoch = node['current_ds_epoch'],
							current_mini_epoch = node['current_mini_epoch'],
							response_time = node['response_time']
						)
						node = await session.execute(select(Node).filter_by(node_name = node['node_name']))
						# session.execute(new_record)
						node.records.append(new_record)
						# session.add(new_node)
						session.add(new_record)
						await session.commit()
					except Exception as ex:
						print(ex)
				try:
					new_node = Node(
						node_url = node['node_url'],
						node_name = node['name'],
					)
					new_record = Records(
						score = 'score',
						update_time = datetime.utcnow().timestamp(),
						current_ds_epoch = node['current_ds_epoch'],
						current_mini_epoch = node['current_mini_epoch'],
						response_time = node['response_time']
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
	engine = create_async_engine('sqlite+aiosqlite:///database.db')
	async_session = async_sessionmaker(engine)
	# asyncio.run(write())
	job = Worker(async_session)
	
	asyncio.run(job.run())