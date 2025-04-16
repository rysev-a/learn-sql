import asyncio

import pytest

from app.database import Database
from app.migrations import init_migrations
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
        await database.fetch("delete from users")
        await database.close()


# @pytest.fixture(scope="session")
# async def admin_headers(db_session):
#     role_repository = await provide_role_repository(db_session)
#     user_repository = await provide_user_repository(db_session)
#     await role_repository.add(RoleModel(name="admin"))
#     await user_repository.create_admin(UserModel(email="admin@mail.com", password=hash_password("admin")))
#
#     async with AsyncTestClient(app) as client:
#         response = await client.post("/api/account/login", json={"email": "admin@mail.com", "password": "admin"})
#         yield {API_KEY_HEADER: f"{TOKEN_PREFIX}{response.json().get('access_token')}"}
#
#     await user_repository.delete_where()
#     await role_repository.delete_where()
#
#
# @pytest.fixture(scope="session")
# async def user_headers(request, db_session):
#     email, password = request.param
#
#     role_repository = await provide_role_repository(db_session)
#     user_repository = await provide_user_repository(db_session)
#
#     await role_repository.add(RoleModel(name="customer"))
#     user = await user_repository.add(UserModel(email=email, password=hash_password(password)))
#
#     await user_repository.add_user_role(user, "customer")
#
#     async with AsyncTestClient(app) as client:
#         response = await client.post("/api/account/login", json={"email": email, "password": password})
#         yield {API_KEY_HEADER: f"{TOKEN_PREFIX}{response.json().get('access_token')}"}
#
#     await user_repository.delete_where()
#     await role_repository.delete_where()
