import asyncio
from requests_module.get_nodes_data import get_total_info
from requests_module.call_url import call_url
from models.models import Node, Records, User, NodesUsers, Blocks
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import lazyload, joinedload
from sqlalchemy import func
from db.engine import get_async_session
import time
from commands.sending_warnings_to_users import send_inactive_node_notifications, send_missed_blocks_notifications
from config.zilliqa import *
from block_worker.blocks_db import BlocksWorker
from logs.logs import init_worker_logger
import logging

# logging.basicConfig(level=logging.INFO)
init_worker_logger('worker')
worker_logger = logging.getLogger('worker.worker_db')

class Worker():

	def __init__(self, async_session):
		self._async_session = async_session

	async def run(self):
		while True:
			await self._write_or_update_node_to_db()
			# await self._checking_the_operation_of_node()
			# time.sleep(10)

	async def _get_last_records(self):
		async with self._async_session() as session:
			records_query = await session.execute(select(Records))
			last_records = records_query.unique().all()
			print(last_records[-28:])

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
			max_curent_ds_epoch = max_curent_ds_epoch_query.unique().one_or_none()
			if max_curent_ds_epoch == None:
				return max_curent_ds_epoch
			return max_curent_ds_epoch[0]
			
	async def _get_max_current_mini_epoch(self):
		blocks_worker = BlocksWorker(async_session)
		max_current_mini_epoch = await blocks_worker._get_max_current_mini_epoch()
		return max_current_mini_epoch

	async def _sending_warnings(self, nodes_users, node_name, missed_blocks):
		try:
			if missed_blocks is not None:
				for user in nodes_users:
					user_telegram_id = user.user_telegram_id
					if user_telegram_id:
						await send_missed_blocks_notifications(user_telegram_id, node_name, missed_blocks)
					else:
						pass
			else:
				for user in nodes_users:
					user_telegram_id = user.user_telegram_id
					if user_telegram_id:
						await send_inactive_node_notifications(user_telegram_id, node_name)
		except Exception as ex:
			worker_logger.debug(ex)

	# async def _searching_for_empty_values_and_delays(self, node, max_mini_epoch):
	# 	node_name = node[0].node_name
	# 	current_ds_epoch = last_record.current_ds_epoch
	# 	current_mini_epoch = last_record.current_mini_epoch
	# 	nodes_users = node[0].nodes_users
	# 	if current_ds_epoch == None:
	# 		args = {
	# 			'node_name': node_name,
	# 			'current_ds_epoch': current_ds_epoch
	# 		}
	# 		await self._sending_warnings(nodes_users, args)
	# 	else:
	# 		if current_mini_epoch < max_mini_epoch - MAX_DIFFERENCE_OF_BLOCKS:
	# 			mini_epoch_diff = max_mini_epoch - current_mini_epoch
	# 			args = {
	# 				'node_name': node_name,
	# 				'current_ds_epoch': current_ds_epoch,
	# 				'mini_epoch_diff': mini_epoch_diff
	# 			}
	# 			await self._sending_warnings(nodes_users, args)			

	async def _checking_the_operation_of_node(self, node, missed_blocks):
		nodes_users = node.nodes_users
		node_name = node.node_name
		try:
			if missed_blocks is not None:
				
				if missed_blocks >= MIN_DIFFERENCE_OF_BLOCKS:
					for user in nodes_users:
						user_telegram_id = user.user_telegram_id
						if user_telegram_id:
							await send_missed_blocks_notifications(
								user_telegram_id,
								node_name,
								missed_blocks
							)
						else:
							pass
			else:
				for user in nodes_users:
					user_telegram_id = user.user_telegram_id
					if user_telegram_id:
						await send_inactive_node_notifications(
							user_telegram_id, 
							node_name
						)
		except Exception as ex:
			# print('checking_the_operation_of_node: ', ex)
			worker_logger.debug(ex)

	async def _buttons(self):
		async with self._async_session() as session:
			buttons_query = await session.execute(select(Node))
			buttons = buttons_query.all()
		return buttons

	async def _get_one_node_from_db(self, node_name):
		async with self._async_session() as session:
			node = await session.execute(select(Node).filter_by(node_name = node_name).options(joinedload(Node.records)))
			node = node.unique().one_or_none()
			if node == None:
				return node
			return node[0]

	async def _get_all_nodes_from_db(self):
		async with self._async_session() as session:
			all_nodes = await session.execute(select(Node).options(joinedload(Node.records)).options(joinedload(Node.nodes_users)))
			all_nodes = all_nodes.unique().all()
			return all_nodes
	
	async def _get_one_user_from_db(self, tg_user_id):
		async with self._async_session() as session:
			user = await session.execute(select(User).filter_by(user_telegram_id = tg_user_id ))
			user = user.unique().one_or_none()
			if user == None:
				return user
			else:
				return user[0]
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
				node = await self._get_one_node_from_db(node_name)
				user = await self._get_one_user_from_db(tg_user_id)
				node.nodes_users.append(user)
				session.add(node)
				await session.commit()
			except Exception as ex:
				line = {
					'line':158
			}
				worker_logger.warning(msg=ex, extra=line)

	async def _create_new_node(self, node_args):
		new_node = Node(
			node_url = node_args['node_url'],
			node_name = node_args['node_name'],
			)
		return new_node

	async def _create_new_record(self, record_args):
		new_record = Records(
			update_time = datetime.utcnow().timestamp(),
			current_ds_epoch = record_args['current_ds_epoch'],
			current_mini_epoch = record_args['current_mini_epoch'],
			response_time = record_args['response_time'],
			rating = record_args['rating'],
			stake_amount = record_args['stake_amount'],
			commission = record_args['commission'],
			number_of_delegates = record_args['number_of_delegates']#
			)
		return new_record

	async def _get_missed_blocks(self, current_mini_epoch):
		max_mini_epoch = await self._get_max_current_mini_epoch()
		if current_mini_epoch is None:
			return None
		missed_blocks_count = max_mini_epoch - current_mini_epoch
		return missed_blocks_count

	async def is_negative(self, missed_blocks):

		if missed_blocks is not None:
			if missed_blocks < 0:
				return 0
			else:
				return missed_blocks
		return missed_blocks

	async def _calculate_entity_score(self, http_response_time, missed_blocks):
		try:
			missed_blocks = await self.is_negative(missed_blocks)
			trust_coefficient = TRUST_COEFFICIENT
			# print(missed_blocks)
			http_time_coefficient = 0.2
			missed_blocks_coefficient = 0.6
			trust_coefficient_coefficient = 0.5
			if missed_blocks is None:
				result = 0
				return result
			if missed_blocks >= MAX_DIFFERENCE_OF_BLOCKS:
				result = 0
				return result
			print('http_response_time', http_response_time)
			print('missed_blocks', missed_blocks)
			normalized_http_time = 1 - http_response_time
			missed_blocks_impact = 1 / (1 + missed_blocks)
			trust_coefficient_impact = trust_coefficient / 100
			result = (
				http_time_coefficient * normalized_http_time +
				missed_blocks_coefficient * missed_blocks_impact +
				trust_coefficient_coefficient * trust_coefficient_impact
			)
			result = min(100, max(0, result * 100))
				# print(result)
			return result
		except Exception as ex:
			worker_logger.debug(ex)

	async def _write_node_db(self, node_from_responce):
		async with self._async_session() as session:
			node_url = node_from_responce['node_url'],
			node_name = node_from_responce['node_name']
			current_ds_epoch = node_from_responce['current_ds_epoch']
			current_mini_epoch = node_from_responce['current_mini_epoch']
			response_time = node_from_responce['response_time']
			stake_amount = node_from_responce['stake_amount']
			commission = node_from_responce['commission']
			number_of_delegates = node_from_responce['number_of_delegates']
			node_db = await self._get_one_node_from_db(node_name)
			if node_db is not None:
				try:
					missed_blocks = await self._get_missed_blocks(current_mini_epoch)
					await self._checking_the_operation_of_node(node_db, missed_blocks)
					rating = await self._calculate_entity_score(response_time, missed_blocks)
					record_args = {
						'current_ds_epoch': current_ds_epoch,
						'current_mini_epoch': current_mini_epoch,
						'response_time': response_time,
						'rating': rating,
						'stake_amount': stake_amount,
						'commission': commission,
						'number_of_delegates': number_of_delegates
				}
					new_record = await self._create_new_record(record_args)
					node_db.records.append(new_record)
					session.add(new_record)
					await session.commit()
				except Exception as ex:
					line = {
						'line':242
					}
					worker_logger.warning(msg=ex, extra=line)
			else:
				try:
					node_args = {
						'node_url': node_url[0],
						'node_name' : node_name
					}
					record_args = {
						'current_ds_epoch': current_ds_epoch,
						'current_mini_epoch': current_mini_epoch,
						'response_time': response_time,
						'rating': 0,
						'stake_amount': '0',
						'commission': '0',
						'number_of_delegates': 0
					}
					new_node = await self._create_new_node(node_args)
					new_record = await self._create_new_record(record_args)
					new_node.records.append(new_record)
					session.add(new_node)
					session.add(new_record)
					await session.commit()
				except Exception as ex:
					line = {
						'line':269
					}
					worker_logger.warning(msg=ex, extra=line)

	async def _write_or_update_node_to_db(self):
		try:
			data = get_total_info()
			for elem in data:
				responce = call_url(elem['node_url'])
				elem['current_ds_epoch'] = responce['current_ds_epoch']
				elem['current_mini_epoch'] = responce['current_mini_epoch']
				elem['response_time'] = responce['response_time']
				await self._write_node_db(elem)
				time.sleep(PAUSE_BETWEEN_REQUESTS)
		except Exception as ex:
			line = {
				'line':285
			}
			worker_logger.warning(msg=ex, extra=line)

if __name__ == '__main__':
	async_session = asyncio.run(get_async_session())
	worker = Worker(async_session)
	# print(asyncio.run(worker._get_node_record()))
	asyncio.run(worker.run())
