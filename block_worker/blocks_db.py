from .get_blocks import get_blocks
from models.models import Blocks
from datetime import datetime
from sqlalchemy import select
from sqlalchemy import func
import time
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
			blocks_logger.warning(msg=ex, extra={'line':25})

	async def _get_max_curent_ds_epoch(self):
		async with self._async_session() as session:
			stmt = select(func.max(Blocks.current_ds_epoch))
			result = await session.execute(stmt)
			max_curent_ds_epoch = result.unique().one_or_none()[0]
			return max_curent_ds_epoch
			
	async def _get_max_current_mini_epoch(self):
		async with self._async_session() as session:
			stmt = select(func.max(Blocks.current_mini_epoch))
			result = await session.execute(stmt)
			max_current_mini_epoch = result.unique().one_or_none()[0]
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
				'response_time': response_time
			}
			new_block = await self._create_new_blocks_record(block_args)
			session.add(new_block)
			blocks_logger.debug('block is recorded', extra={'line':62})
			await session.commit()
