import asyncio
from db import init_db
from tortoise import Tortoise

async def main():
    await init_db()
    print("DB Connected ✅")
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(main())