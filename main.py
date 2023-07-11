from aiogram import Dispatcher, Bot
import asyncio
import logging
import os
from commands import register_user_comands
from commands.bot_commands import bot_commands
from aiogram.types import BotCommand
# from db import async_session
from midelwares import RegisterCheck
from aiogram import BaseMiddleware
from worker.worker_db import Worker
import threading
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

async def bot():
    engine = create_async_engine('sqlite+aiosqlite:///database.db')
    async_session = async_sessionmaker(engine)
    logging.basicConfig(level=logging.INFO)
    #Gen commands menu
    comands_for_bot = []
    for cmd in bot_commands:
        comands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    dp = Dispatcher()
    bot = Bot(token=os.getenv('NODE_TOKEN'))
    #Set commands
    await bot.set_my_commands(commands=comands_for_bot)
    awaitregister_user_comands(dp)
    await dp.start_polling(bot, async_session=async_session)

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.run(bot())

# def between_callback():
#     worker = Worker(async_session)
#     asyncio.run(worker.run())
#     # loop = asyncio.new_event_loop()
#     # asyncio.set_event_loop(loop)
#     # loop.run_until_complete(bot())
#     # loop.close()

def process_data_in_thread():
    thread_id = threading.get_ident()
    print(f'Запуск потока {thread_id}')
    run_bot()
    print(f'Завершение потока {thread_id}')

async def process_data_async():
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, process_data_in_thread)
    await future

async def main():
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(process_data_async())]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
   
    try:

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
        # _thread = threading.Thread(target=run_bot,)
        # # _thread2 = threading.Thread(target=between_callback)
        # _thread.start()
        # _thread2.start()
        # print(threading.active_count())
        
    except (KeyboardInterrupt, SystemExit):
        
        print('bot stoped')
        