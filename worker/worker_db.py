import asyncio
from requests_module.get_nodes_data import get_total_info
from requests_module.call_url import call_url
from models.models import Node, Records, User, NodesUsers
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from db.engine import get_async_session
import time
from commands.sending_warnings_to_users import send_inactive_node_notifications
from commands.sending_warnings_to_users import send_missed_blocks_notifications
from config.zilliqa import TRUST_COEFFICIENT
from config.zilliqa import MIN_DIFFERENCE_OF_BLOCKS
from config.zilliqa import MAX_DIFFERENCE_OF_BLOCKS
from config.zilliqa import PAUSE_BETWEEN_REQUESTS
from block_worker.blocks_db import BlocksWorker
from logs.logs import init_worker_logger
import logging
from typing import List, Union

init_worker_logger('worker')
worker_logger = logging.getLogger('worker.worker_db')


class Worker():
	def __init__(self, async_session):
		self._async_session = async_session

	async def run(self):
		while True:
			await self._write_or_update_node_to_db()

	async def _delete_user_from_user_nodes(
		self,
		node_name: str, 
		tg_user_id: int
		) -> bool:
		async with self._async_session() as session:
			node = await self._get_one_node_from_db(node_name)
			user = await self._get_one_user_from_db(tg_user_id)
			if node is not None and user is not None:
				stmt = select(NodesUsers).where(
					NodesUsers.node_id == node.node_id, 
					NodesUsers.user_id == user.user_id
				)
				responce = await session.execute(stmt)
				nodes_user = responce.unique().one_or_none()
				if nodes_user is not None:
					await session.delete(nodes_user[0])
					await session.commit()
					return True
				else:
					return False
			return False

	async def _get_max_curent_ds_epoch(self) -> int:
		async with self._async_session() as session:
			stmt = select(func.max(Records.current_ds_epoch))
			responce = await session.execute(stmt)
			max_curent_ds_epoch = responce.unique().one_or_none()
			if max_curent_ds_epoch == None:
				return max_curent_ds_epoch
			return max_curent_ds_epoch[0]
			
	async def _get_max_current_mini_epoch(self) -> Union[int, None]:
		blocks_worker = BlocksWorker(async_session)
		result = await blocks_worker._get_max_current_mini_epoch()
		return result

	async def _sending_warnings(
		self, 
		nodes_users: List[User], 
		node_name: str, 
		missed_blocks: int
		) -> None:
		try:
			if missed_blocks is not None:
				for user in nodes_users:
					user_telegram_id = int(user.user_telegram_id)
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
			worker_logger.debug(ex, extra={'line':96})

	async def _checking_the_operation_of_node(
		self, 
		node: Node, 
		missed_blocks: int
	) -> None:
		nodes_users = node.nodes_users
		node_name = str(node.node_name)
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
			worker_logger.debug(ex, extra={'line':123})

	async def _buttons(self) -> List[Node]:
		async with self._async_session() as session:
			result = await session.execute(select(Node))
			buttons = result.all()
		return buttons

	async def _get_one_node_from_db(self, node_name: str) -> Node|None:
		async with self._async_session() as session:
			stmt = select(Node).filter_by(
				node_name = node_name
				).options(joinedload(Node.records))
			result = await session.execute(stmt)
			node = result.unique().one_or_none()
			if node is None:
				return None
			return node[0]

	async def _get_all_nodes_from_db(self) -> List[Node]:
		async with self._async_session() as session:
			stmt = select(Node).options(
				joinedload(Node.records)
			).options(joinedload(Node.nodes_users))
			result = await session.execute(stmt)
			all_nodes = result.unique().all()
			return all_nodes
	
	async def _get_one_user_from_db(self, tg_user_id: int) -> Node|None:
		async with self._async_session() as session:
			stmt = select(User).filter_by(user_telegram_id = tg_user_id)
			result = await session.execute(stmt)
			user = result.unique().one_or_none()
			if user is None:
				return None
			else:
				return user[0]

	async def _get_nodes_users(self, node_name, ):
		async with self._async_session() as session:
			stmt = select(Node).options(
				joinedload(Node.nodes_users)
			).filter_by(node_name = node_name )
			result = await session.execute(stmt)
			node = result.first()[0]
			nodes_users = node.nodes_users
			return nodes_users
			
	async def _check_subscribe(self, node_name, tg_user_id):
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
				worker_logger.warning(msg=ex, extra={'line':191})

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
		if missed_blocks is not None and missed_blocks < 0:
			return 0
		return missed_blocks


	async def _calculate_entity_score(
		self, 
		http_response_time, 
		missed_blocks
	):
		try:
			missed_blocks = await self.is_negative(missed_blocks)
			trust_coefficient = TRUST_COEFFICIENT
			http_time_coefficient = 0.2
			missed_blocks_coefficient = 0.6
			trust_coefficient_coefficient = 0.5
			if missed_blocks is None:
				result = 0
				return result
			if missed_blocks >= MAX_DIFFERENCE_OF_BLOCKS:
				result = 0
				return result
			normalized_http_time = 1 - http_response_time
			missed_blocks_impact = 1 / (1 + missed_blocks)
			trust_coefficient_impact = trust_coefficient / 100
			result = (
				http_time_coefficient * normalized_http_time +
				missed_blocks_coefficient * missed_blocks_impact +
				trust_coefficient_coefficient * trust_coefficient_impact
			)
			result = min(100, max(0, result * 100))
			return result
		except Exception as ex:
			worker_logger.warning(msg=ex, extra={'line':256})

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
					missed_blocks = await self._get_missed_blocks(
						current_mini_epoch
					)
					await self._checking_the_operation_of_node(
						node_db, missed_blocks
					)
					rating = await self._calculate_entity_score(
						response_time, 
						missed_blocks
					)
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
					worker_logger.warning(msg=ex, extra={'line':295})
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
					worker_logger.warning(msg=ex, extra={'line':318})

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
			worker_logger.warning(msg=ex, extra={'line':331})

if __name__ == '__main__':
	async_session = asyncio.run(get_async_session())
	worker = Worker(async_session)
	asyncio.run(worker.run())
