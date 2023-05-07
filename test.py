Не надо использовать цикл while в асинхронном коде, да и в целом если бот рассчитан на более чем одного пользователя
Используйте storage

from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()


from aiogram.dispatcher import FSMContext

@dp.message_handler(commands=['start'])
async def start(message: types.Message,  state=FSMContext):
    await message.answer('Вы ввели команду /start, введите команду /stop или /cancel чтобы выйти из меню')
    await state.set_state(YourState.name_state)

@dp.message_handler(commands=['stop'], state=YourState.name_state)
async def stop(message: types.Message,  state=FSMContext):
    await message.answer('Вы ввели команду /stop')
    await state.finish()

@dp.message_handler(commands=['cancel'], state='*')
async def cancel(message: types.Message,  state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Вы ввели команду /cancel'