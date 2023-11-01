from migrations.alembic_config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

url_db: str = "postgresql+asyncpg://" + (DB_USER or "") + ":" + (DB_PASSWORD or "") + "@" + (DB_HOST or "") + "/" + (DB_NAME or "")
