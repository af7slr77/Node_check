import asyncio
from lib.get_nodes_info import get_nodes_info
from lib.get_nodes_urls import get_nodes_urls
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import Node, Records, User # UsersNodes
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import lazyload, joinedload

from db import async_session


class Worker():
	interval = 10000
	_async_session = None
	# _node_name = None


	def __init__(self, async_session):
		self._async_session = async_session
		# self._node_name = node_name

	async def run(self):
		try:
			nodes_info = await self._fetch_nodes()
			await self._update_node_db(nodes_info)
		except Exception as ex:
			print('run worker job error: ',  ex)
	
	async def _fetch_nodes(self):
		urls = get_nodes_urls()
		nodes_info = await get_nodes_info(urls)
		return nodes_info

	async def _get_one_node_from_db(self, node_name):
		async with self._async_session() as session:
			node = await session.execute(select(Node).filter_by(node_name = node_name).options(joinedload(Node.records)))
			node = node.unique().one_or_none()[0]
			return node

	async def _get_all_nodes_from_db(self):
		async with self._async_session() as session:
			all_nodes = await session.execute(select(Node).options(joinedload(Node.records)))
			all_nodes = all_nodes.unique().all()
			return all_nodes

	async def _check_new_blocks(self, node_from_db, node_from_responce):
			try:
				last_block_record = node_from_db.records[-1]
				db_current_ds_epoch = last_block_record.current_ds_epoch
				db_current_mini_epoch = last_block_record.current_mini_epoch
				if db_current_mini_epoch == node_from_responce['current_mini_epoch']:
					print(db_current_mini_epoch, node_from_responce['current_mini_epoch'], db_current_mini_epoch == node_from_responce['current_mini_epoch'])
					return True
				else:
					print(db_current_mini_epoch, node_from_responce['current_mini_epoch'], db_current_mini_epoch == node_from_responce['current_mini_epoch'])
					return False
			except Exception as ex:
					print('_check_new_blocks - func', ex,)
	
	async def _get_one_user_from_db(self, tg_user_id):
		async with self._async_session() as session:
			user = await session.execute(select(User).filter_by(user_telegram_id = tg_user_id ))
			user = user.unique().one_or_none()[0]
			return user

	async def _subscribe(self, node_name, tg_user_id):
		
		async with self._async_session() as session:
			node = await session.execute(select(Node).filter_by(node_name = node_name).options(joinedload(Node.records)))
			node = node.unique().one_or_none()[0]
			user = await session.execute(select(User).filter_by(user_telegram_id = tg_user_id ))
			user = user.unique().one_or_none()[0]
			
			node.users.append(user)
			session.add(node)
			await session.commit()

	async def _update_node_db(self, nodes_info):
		async with self._async_session() as session:
			for node_from_responce in nodes_info:
				try:
					node_db = await session.execute(select(Node).filter_by(node_name = node_from_responce['node_name']))
					node_db = node_db.one_or_none()[0].node_name
					if node_db == node_from_responce['node_name']:
						# print('update exists node')
						try:
							node_from_db = await session.execute(select(Node).filter_by(node_name = node_from_responce['node_name']).options(joinedload(Node.records)))
							node_from_db = node_from_db.first()[0] 
							new_record = Records(
							score = 'score',
							update_time = datetime.utcnow().timestamp(),
							current_ds_epoch = node_from_responce['current_ds_epoch'],
							current_mini_epoch = node_from_responce['current_mini_epoch'],
							response_time = node_from_responce['response_time']
						)
							node_from_db.records.append(new_record)
							session.add(new_record)
							await session.commit()
						except Exception as ex:
							print('_update_db, if node_db', ex)
				except Exception as ex:
					print(ex)
					try:
						# print('create new node')
						new_node = Node(
							node_url = node_from_responce['node_url'],
							node_name = node_from_responce['node_name'],
						)
						new_record = Records(
							score = 'score',
							update_time = datetime.utcnow().timestamp(),
							current_ds_epoch = node_from_responce['current_ds_epoch'],
							current_mini_epoch = node_from_responce['current_mini_epoch'],
							response_time = node_from_responce['response_time']
						)
						new_node.records.append(new_record)
						session.add(new_node)
						session.add(new_record)
						await session.commit()
					except Exception as ex:
						print('_update_db, else if node_db',  ex)
					

				
if __name__ == '__main__':
	job = Worker(async_session)
	asyncio.run(job.run())