import os
from migrations.alembic_config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

url_db= "postgresql+asyncpg://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_HOST + "/" + DB_NAME
