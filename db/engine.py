from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

engine = create_async_engine('sqlite+aiosqlite:///database.db')
async_session = async_sessionmaker(engine)

