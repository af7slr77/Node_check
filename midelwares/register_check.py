import asyncio
from typing import Callable, Dict, Any, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
# from db.engine import async_session
from models.models import Node, User
from sqlalchemy import select
from sqlalchemy.orm import lazyload, joinedload
from datetime import datetime

class RegisterCheck(BaseMiddleware):
	async def __call__(
		self,
		handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
		event: Union[Message, CallbackQuery],
		data: Dict[str, Any] 
	) -> Any:
		async_session: async_session = data['async_session']
		async with async_session() as session:
			result = await session.execute(select(User).where(User.user_telegram_id == event.from_user.id))
			user = result.one_or_none()
			if user is not None:
				pass
			else:
				try:
					new_user = User(
						user_telegram_id = event.from_user.id,
						username = event.from_user.username,
						reg_date = datetime.utcnow().timestamp()
					)
					session.add(new_user)
					await session.commit()
				except Exception as ex:
					print('RegisterCheck',  ex)
		return await handler(event, data)
