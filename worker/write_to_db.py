import asyncio
from lib.get_nodes_info import get_nodes_info
from lib.get_nodes_urls import get_nodes_urls
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import Node, Records
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import lazyload, joinedload

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
				try:
					node_db = await session.execute(select(Node).filter_by(node_name = node['node_name']))
					node_db = node_db.one_or_none()[0].node_name
					if node_db == node['node_name']:
						print('update exists node')
						try:
							new_record = Records(
								score = 'score',
								update_time = datetime.utcnow().timestamp(),
								current_ds_epoch = node['current_ds_epoch'],
								current_mini_epoch = node['current_mini_epoch'],
								response_time = node['response_time']
							)
							node = await session.execute(select(Node).filter_by(node_name = node['node_name']).options(joinedload(Node.records)))
							node = node.first()[0]
							print(node)
							node.records.append(new_record)
							session.add(new_record)
							await session.commit()
						except Exception as ex:
							print('_update_db, if node_db', ex)
				except Exception as ex:
					print(ex)
					try:
						print('create new node')
						new_node = Node(
							node_url = node['node_url'],
							node_name = node['node_name'],
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
						print('_update_db, else if node_db',  ex)
					

				
if __name__ == '__main__':
	engine = create_async_engine('sqlite+aiosqlite:///database.db')
	async_session = async_sessionmaker(engine)
	job = Worker(async_session)
	
	
	asyncio.run(job.run())