from .auth import create_auth_tables


async def init_migrations(execute):
    await create_auth_tables(execute)
