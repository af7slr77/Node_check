import asyncio
from query_modules.get_nodes_info import get_nodes_info
from query_modules.get_nodes_urls import get_nodes_urls
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import Node, Records, User, NodesUsers
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import lazyload, joinedload
from sqlalchemy import func
from db import async_session
import time
from commands.sending_warnings_to_users import sending_warnings_to_users


class Worker():
	interval = 10000
	_async_session = None

	def __init__(self, async_session):
		self._async_session = async_session

	async def run(self):
		try:
			# while True:
				nodes_info = await self._fetch_nodes()
				await self._update_node_db(nodes_info)
				await self._checking_the_operation_of_node()
				time.sleep(30)
			
		except Exception as ex:
			print('run worker job error: ',  ex)

	async def _delete_user_from_user_nodes(self, node_name, tg_user_id):
		async with self._async_session() as session:
			node = await self._get_one_node_from_db(node_name)
			user = await self._get_one_user_from_db(tg_user_id)
			nodes_user_query = await session.execute(select(NodesUsers).filter_by(node_id=node.node_id))
			nodes_user = nodes_user_query.unique().one_or_none()[0]
			await session.delete(nodes_user)
			await session.commit()

	async def _get_max_curent_ds_epoch(self):
		async with self._async_session() as session:
			max_curent_ds_epoch_query = await session.execute(select(func.max(Records.current_ds_epoch)))
			max_curent_ds_epoch = max_curent_ds_epoch_query.unique().one_or_none()[0]
			return max_curent_ds_epoch
			
	async def _get_max_current_mini_epoch(self):
		async with self._async_session() as session:
			max_curent_ds_epoch_query = await session.execute(select(func.max(Records.current_mini_epoch)))
			max_current_mini_epoch = max_curent_ds_epoch_query.unique().one_or_none()[0]
			return max_current_mini_epoch

	async def _checking_the_operation_of_node(self):
		async with self._async_session() as session:
			max_ds_epoch = await self._get_max_curent_ds_epoch()
			max_mini_epoch = await self._get_max_current_mini_epoch()
			all_nodes =  await self._get_all_nodes_from_db()
			for node in all_nodes:
				node_name = node[0].node_name
				last_record = node[0].records[-1]
				current_ds_epoch = last_record.current_ds_epoch
				current_mini_epoch = last_record.current_mini_epoch
				nodes_users = node[0].nodes_users
				if current_ds_epoch == None:
					for user in nodes_users:
						tg_user_id = user.user_telegram_id
						args = {
							'node_name': node_name,
							'current_ds_epoch': current_ds_epoch
						}
						# print(args)
						await sending_warnings_to_users(tg_user_id, args)

					# if current_ds_epoch < max_ds_epoch - 1:
					# 	for user in nodes_users:
					# 		tg_user_id = user.user_telegram_id
					# 		ds_epoch_diff = max_ds_epoch - current_ds_epoch
					# 		args = {
					# 			'node_name': node_name,
					# 			'current_ds_epoch': current_ds_epoch,
					# 			'ds_epoch_diff': ds_epoch_diff
					# 		}
					# 		# await sending_warnings_to_users(tg_user_id, args)
					
				else:
					# print(nodes_users)
					if current_mini_epoch < max_mini_epoch - 1:
						for user in nodes_users:
							tg_user_id = user.user_telegram_id
							
							mini_epoch_diff = max_mini_epoch - current_mini_epoch
							# print(mini_epoch_diff)
							args = {
								'node_name': node_name,
								'current_ds_epoch': current_ds_epoch,
								'mini_epoch_diff': mini_epoch_diff
							}
							# print(args)
						await sending_warnings_to_users(tg_user_id, args)
					
					# print(current_ds_epoch)

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
			all_nodes = await session.execute(select(Node).options(joinedload(Node.records)).options(joinedload(Node.nodes_users)))
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

	async def _get_nodes_users(self, node_name, ):
		async with self._async_session() as session:
			node_query = await session.execute(select(Node).options(joinedload(Node.nodes_users)).filter_by(node_name = node_name ))
			node = node_query.first()[0]
			nodes_users = node.nodes_users
			return nodes_users
			
	async def _check_subscribe(self, node_name, tg_user_id):
		"""This func check subscribe"""
		nodes_users = await self._get_nodes_users(node_name)
		for user in nodes_users:
			tg_user_id_from_db = user.user_telegram_id
			if tg_user_id_from_db == tg_user_id:
				return True
			else:
				continue
		return False

	async def _subscribe(self, node_name, tg_user_id):
		async with self._async_session() as session:
			try:
				node_query = await session.execute(select(Node).filter_by(node_name = node_name))#.options(joinedload(Node.records)))
				node = node_query.unique().one_or_none()[0]
				user_query = await session.execute(select(User).filter_by(user_telegram_id = tg_user_id ))
				user = user_query.unique().one_or_none()[0]
				node.nodes_users.append(user)
				session.add(node)
				await session.commit()

			except Exception as ex:
				print('worker.subscribe ', ex)

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
					

				
# if __name__ == '__main__':
# 	job = Worker(async_session)
# 	asyncio.run(job.run())