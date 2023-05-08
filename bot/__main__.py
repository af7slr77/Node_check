from aiogram import Dispatcher, Bot
import asyncio
import logging
import os
from commands import register_user_comands
from commands.bot_commands import bot_commands
from aiogram.types import BotCommand
from db import BaseModel, get_session_maker, create_async_engine, proseed_schemas


async def main():
    logging.basicConfig(level=logging.DEBUG)

    #Gen commands menu
    comands_for_bot = []
    for cmd in bot_commands:
        comands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    dp = Dispatcher()
    bot = Bot(token=os.getenv('NODE_TOKEN'))
    #Set commands
    await bot.set_my_commands(commands=comands_for_bot)
    register_user_comands(dp)
    

    async_engine = create_async_engine("sqlite:///db.new_db")
    session_maker = get_session_maker(async_engine)
    await proseed_schemas(async_engine, BaseModel.metadata)

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('bot stoped')