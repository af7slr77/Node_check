from aiogram import types
from db import async_session
from worker import Worker


async def sent_nodes_info(call: types.CallbackQuery):
    node_name = call.data
    # print(node_name)
    node_data = Worker(async_session)
    node_data = await node_data._get_one_node_from_db(node_name)
    print(node_data)
    a = 'fdgdf'
    msg = "Вот что я нашёл:\n" f"URL: {a}\n" f"E-mail: {a}\n "f"Пароль: {a}"
    await call.message.answer(text=msg)