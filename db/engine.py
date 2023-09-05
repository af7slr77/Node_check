from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
import os

async def get_async_session():
	async_engine = create_async_engine("postgresql+asyncpg://" + os.getenv("DB_USER") + ":" + os.getenv("DB_PASSWORD") + "@" + os.getenv("DB_HOST") + "/" + os.getenv("DB_NAME"))
	async_session = async_sessionmaker(
		async_engine, class_=AsyncSession, expire_on_commit=False, autocommit=False
	)
	return async_session