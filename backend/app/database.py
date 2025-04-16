import asyncpg


class Database:
    def __init__(self) -> None:
        self.connection = None
        self.pool = None

    async def connect(self, db_uri: str, pool_db: str):
        self.connection = await asyncpg.connect(db_uri)
        self.pool = await asyncpg.create_pool(database=pool_db)

    async def close(self):
        await self.pool.close()
        await self.connection.close()

    async def fetch(self, *args):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                return await connection.fetch(*args)

    async def fetch_row(self, *args):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                return await connection.fetchrow(*args)

    async def execute_many(self, *args):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                return await connection.executemany(*args)
