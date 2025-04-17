from app.auth.migrations.auth import create_auth_tables, drop_auth_tables


async def init_migrations(execute):
    await create_auth_tables(execute)


async def teardown_migrations(execute):
    await drop_auth_tables(execute)
