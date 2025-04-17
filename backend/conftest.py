import asyncio

import pytest

from app.database import Database
from app.migrations import init_migrations, teardown_migrations
from app.settings import settings


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")  # I add the following fixture to configure asyncio in pytest
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def db():
    # 1. connect
    database = Database()
    await database.connect(settings.db_uri, settings.pool_db)

    # 2. add migrations
    await init_migrations(database.fetch)

    # 2. create async engine
    try:
        yield database
    except Exception as e:
        raise e
    finally:
        # 3. clear database
        await teardown_migrations(database.fetch)
        await database.close()
