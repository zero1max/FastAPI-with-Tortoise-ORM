import os
from tortoise import Tortoise
from config import get_settings

settings = get_settings()

# DATABASE_URL = f'postgres://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'
DB_PATH = os.path.abspath(f"{settings.db_name}.db")

print("SQLite file path:", DB_PATH)

DATABASE_URL = f"sqlite:///{DB_PATH}"
# DB_URL = "postgresql://neondb_owner:npg_7t0mlTwduAis@ep-winter-meadow-a18p3t4g-pooler.ap-southeast-1.aws.neon.tech/tor_orm?sslmode=require"

DB_CONFIG = {
    "connections": {
        "default": f"{DATABASE_URL}",
    },
    "apps": {
        "models": {
            "models": ["models.user","models.book", "aerich.models"],
            "default_connection": "default",
        }
    }
}


async def init_db():
    await Tortoise.init(config=DB_CONFIG)