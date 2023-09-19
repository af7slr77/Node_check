import asyncio
import logging
from db.engine import get_async_session
from block_worker.blocks_db import BlocksWorker
from logs.logs import init_worker_logger 

init_worker_logger('worker')
run_worker_logger = logging.getLogger('worker.run_worker')

def main():
	async_session = asyncio.run(get_async_session())
	block = BlocksWorker(async_session=async_session)
	asyncio.run(block.run())

if __name__ == '__main__':
	try:
		main()
	except Exception as ex:
		run_worker_logger.warning(msg=ex, extra={'line':23})