from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

async def get_async_session():
	async_engine = create_async_engine('postgresql+asyncpg://andrey:123@localhost/bot_db')
	async_session = async_sessionmaker(
		async_engine, class_=AsyncSession, expire_on_commit=False, autocommit=False
	)
	return async_session