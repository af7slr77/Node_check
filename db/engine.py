from typing import Union
from sqlalchemy.ext.asyncio import create_async_engine as _create_assync_engine, AsyncSession
from sqlalchemy.engine import URL 
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker

async def create_async_engine(url: Union[URL, str]):
    return _create_assync_engine(url=url, echo=True,  pool_pre_ping=True)

# async def proseed_schemas(engine:AsyncEngine, metadata):
#     async with engine.begin() as conn:
#         await conn.run_sync(metadata.create_all)

# def get_session_maker(engine:AsyncEngine) -> sessionmaker:
#     return sessionmaker(engine, class_=AsyncSession)

async def get_session_maker(engine:AsyncEngine):
    return async_sessionmaker(engine, class_=AsyncSession)