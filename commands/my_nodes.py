from aiogram import types
from db import async_session
from worker.worker_db import Worker
from .callbacks import MyNodesCallback

async def my_nodes(call: types.CallbackQuery, callback_data: MyNodesCallback):
    node_name = callback_data.node_name
    tg_user_id = call.from_user.id
    worker = Worker(async_session)
    user = await worker._get_one_user_from_db(tg_user_id)
    users_nodes = user.users_nodes
    msg = ''
    count = 0
    for node in users_nodes:
        msg = msg + f"{node.node_name}\n"
        count += 1
        if count == len(users_nodes):
            await call.message.answer(text=msg)
        else:
            pass