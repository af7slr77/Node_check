from typing import Callable, Dict, Any, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from models.models import User
from sqlalchemy import select
from datetime import datetime
import logging
from logs.logs import init_register_check_logger

init_register_check_logger("register_check")
register_check_logger = logging.getLogger('register_check')


class RegisterCheck(BaseMiddleware):
	async def __call__(
		self,
		handler: Callable[
			[Message, Dict[str, Any]], 
			Awaitable[Any]
		],
		event: Union[Message, CallbackQuery],
		data: Dict[str, Any] 
	) -> Any:
		async_session: async_session = data['async_session']
		async with async_session() as session:
			stmt = select(User).where(
				User.user_telegram_id == event.from_user.id
			)
			result = await session.execute(stmt)
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
					blocks_logger.debug(ex, extra={'line':42})
		return await handler(event, data)
