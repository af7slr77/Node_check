import asyncio
from .get_blocks import get_blocks
from models.models import Blocks
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import lazyload, joinedload
from sqlalchemy import func
from db.engine import get_async_session
import time
from config import MAX_DIFFERENCE_OF_BLOCKS, MIN_DIFFERENCE_OF_BLOCKS, MAX_RESPONSE_SECONDS, MIN_RESPONSE_SECONDS, AVERAGE_RESPONSE_SECONDS
import logging
from logs.logs import init_block_logger

init_block_logger('block')
blocks_logger = logging.getLogger('block.block_worker.block_db')


class BlocksWorker():

	def __init__(self, async_session):
		self._async_session = async_session

	async def run(self):
		try:
			while True:
				block_info = get_blocks()
				await self._write_block_db(block_info)
				time.sleep(5)
		except Exception as ex:
			line = {
				'line':35
				}
			blocks_logger.warning(msg=ex, extra=line)


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
			line = {
				'line':70
				}
			blocks_logger.debug('block is recorded', extra=line)
			await session.commit()

if __name__ == '__main__':
	async_session = asyncio.run(get_async_session())
	block = BlocksWorker(async_session)
	asyncio.run(block.run())