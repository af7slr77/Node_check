import asyncio
import logging
import os
from commands.bot_commands import bot_commands
from db.engine import async_session
from worker.worker_db import Worker
from logs.logs import init_logger 

init_logger('worker')
run_worker_logger = logging.getLogger('worker.run_worker')
call_url_logger = logging.getLogger('worker.run_worker')

async def main():
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