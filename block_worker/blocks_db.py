import asyncio
from query_modules_2.get_nodes_info import get_nodes_info
from .get_blocks import get_blocks
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import Node, Records, User, NodesUsers, Blocks
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import lazyload, joinedload
from sqlalchemy import func
from db import async_session
import time
from commands.sending_warnings_to_users import sending_warnings_to_users
from config import MAX_DIFFERENCE_OF_BLOCKS, MIN_DIFFERENCE_OF_BLOCKS, MAX_RESPONSE_SECONDS, MIN_RESPONSE_SECONDS, AVERAGE_RESPONSE_SECONDS


class BlocksWorker():
	interval = 10000
	_async_session = None

	def __init__(self, async_session):
		self._async_session = async_session

	async def run(self):
		try:
			while True:
				nodes_info = await self._fetch_nodes()
				# await self._write_or_update_node_to_db(nodes_info)
				time.sleep(5)
			
		except Exception as ex:
			print('run block worker job error: ',  ex)


	async def _get_max_curent_ds_epoch(self):
		async with self._async_session() as session:
			max_curent_ds_epoch_query = await session.execute(select(func.max(Blocks.current_ds_epoch)))
			max_curent_ds_epoch = max_curent_ds_epoch_query.unique().one_or_none()[0]
			return max_curent_ds_epoch
			
	async def _get_max_current_mini_epoch(self):
		async with self._async_session() as session:
			max_curent_ds_epoch_query = await session.execute(select(func.max(Blocks.current_mini_epoch)))
			max_current_mini_epoch = max_curent_ds_epoch_query.unique().one_or_none()[0]
			return max_current_mini_epoch

	async def _cereate_new_blocks_record(self, record_args):
		new_record = Records(
			update_time = datetime.utcnow().timestamp(),
			current_ds_epoch = record_args['current_ds_epoch'],
			current_mini_epoch = record_args['current_mini_epoch'],
			response_time = record_args['response_time']
			)
		return new_record

	async def _write_block_db(self, node_from_responce):
		async with self._async_session() as session:
			node_url = node_from_responce['node_url'],
			node_name = node_from_responce['node_name']
			current_ds_epoch = node_from_responce['current_ds_epoch']
			current_mini_epoch = node_from_responce['current_mini_epoch']
			response_time = node_from_responce['response_time']
			node_db = await self._get_one_node_from_db(node_from_responce['node_name'])
			if node_db is not None:
				node_name = node_db.node_name
				max_mini_epoch = int(await self._get_max_current_mini_epoch())
				last_score_from_db = int(await self._get_last_node_score(node_name))
				current_responce_score = await self._current_score(current_mini_epoch, response_time, max_mini_epoch)
				score = last_score_from_db + current_responce_score
				rating = round(await self._get_rating(node_name, last_score_from_db))
				record_args = {
					'current_ds_epoch': current_ds_epoch,
					'current_mini_epoch': current_mini_epoch,
					'response_time': response_time,
					'score': last_score_from_db,
					'rating': rating
				}
				new_record = await self._cereate_new_record(record_args)
				node_db.records.append(new_record)
				session.add(new_record)
				await session.commit()
			else:
				node_args = {
					'node_url': node_url,
					'node_name' : node_name
				}

				record_args = {
					'current_ds_epoch': current_ds_epoch,
					'current_mini_epoch': current_mini_epoch,
					'response_time': response_time,
					'score': 0,
					'rating': 0
				}
				new_node = await self._cereate_new_record(node_args)
				new_record = await self._cereate_new_record(record_args)
				new_node.records.append(new_record)
				session.add(new_node)
				session.add(new_record)
				await session.commit()

	async def _write_or_update_node_to_db(self, nodes_info):
		for node_from_responce in nodes_info:
			try:
				await self._write_node_db(node_from_responce)
			except Exception as ex:
				print('exeption',  ex)
