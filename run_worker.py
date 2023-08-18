import asyncio
import logging
import os
from commands.bot_commands import bot_commands
from db.engine import get_async_session
from worker.worker_db import Worker
from logs.logs import init_worker_logger 

init_worker_logger('worker')
run_worker_logger = logging.getLogger('worker.run_worker')
call_url_logger = logging.getLogger('worker.run_worker')

async def main():
	async_session = await get_async_session()
	worker = Worker(async_session)
	await worker.run()


if __name__ == '__main__':
	try:
		asyncio.run(main())
	except Exception as ex:
		line = {
			'line':25
		}
		run_worker_logger.warning(msg=ex, extra=line)