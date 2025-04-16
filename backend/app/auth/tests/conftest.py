from typing import List

import pytest

from lab.auth.auth_core import hash_password

from app.auth.auth_cli import load_users_fixtures
from app.auth.services.user_service import UserModel, UserService
from app.database import Database


@pytest.fixture(scope="session")
async def test_user_data():
    return UserModel(
        email="test_user@mail.com",
        first_name="Test",
        last_name="User",
        password=hash_password("test_user_password"),
    )


@pytest.fixture(scope="function")
async def test_users(db: Database) -> List[UserModel]:
    await load_users_fixtures(db)
    yield [UserModel(**user) for user in await db.fetch("SELECT * FROM users")]
    await db.fetch("delete from users")


@pytest.fixture(scope="function")
async def test_user(db: Database, test_user_data: UserModel) -> UserModel:
    user = UserModel(
        **await db.fetch_row(
            "INSERT INTO users (email, first_name, last_name, password) VALUES ($1, $2, $3, $4) returning *",
            test_user_data.email,
            test_user_data.first_name,
            test_user_data.last_name,
            test_user_data.password,
        )
    )
    yield user
    await db.fetch_row("delete from users where id=$1", user.id)


@pytest.fixture(scope="function")
async def user_service(db: Database):
    return UserService(db)
