import asyncio
from .get_blocks import get_blocks
from db.base import Node, Records, User, NodesUsers, Blocks
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import lazyload, joinedload
from sqlalchemy import func
from db import async_session
import time
from config import MAX_DIFFERENCE_OF_BLOCKS, MIN_DIFFERENCE_OF_BLOCKS, MAX_RESPONSE_SECONDS, MIN_RESPONSE_SECONDS, AVERAGE_RESPONSE_SECONDS


class BlocksWorker():

	def __init__(self, async_session):
		self._async_session = async_session

	async def run(self):
		try:
			while True:
				block_info = get_blocks()
				print(block_info)
				await self._write_block_db(block_info)
				# print(await self._get_max_current_mini_epoch())
				time.sleep(10)
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

	async def _create_new_blocks_record(self, record_args):
		new_block = Blocks(
			update_time = datetime.utcnow().timestamp(),
			current_ds_epoch = record_args['current_ds_epoch'],
			current_mini_epoch = record_args['current_mini_epoch'],
			response_time = record_args['response_time']
			)
		return new_block

	async def _write_block_db(self, block_from_responce):
		async with self._async_session() as session:
			current_ds_epoch = block_from_responce['current_ds_epoch']
			current_mini_epoch = block_from_responce['current_mini_epoch']
			response_time = block_from_responce['response_time']
			block_args = {
				'current_ds_epoch': current_ds_epoch,
				'current_mini_epoch': current_mini_epoch,
				'response_time': response_time,
			}
			new_block = await self._create_new_blocks_record(block_args)
			session.add(new_block)
			print('block is recorded')
			await session.commit()
if __name__ == '__main__':
	block = BlocksWorker(async_session)
	asyncio.run(block.run())