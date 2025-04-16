from litestar.testing import AsyncTestClient
import pytest

from app.auth.services.user_service import UserModel
from app.main import app


async def test_get_users(test_users):
    async with AsyncTestClient(app) as client:
        response = await client.get("/api/users")
        assert len(response.json()) == 500


async def test_get_first_10_users(test_users):
    async with AsyncTestClient(app) as client:
        response = await client.get("/api/users?limit=10")
        assert len(response.json()) == 10


@pytest.mark.parametrize(
    "offset,limit",
    [
        (100, 10),
        (250, 85),
        (10, 100),
        (85, 250),
    ],
)
async def test_10_users_with_100_offset(test_users, offset, limit):
    async with AsyncTestClient(app) as client:
        response = await client.get(f"/api/users?limit={limit}&offset={offset}")
        assert list(map(lambda user: UserModel(**user), response.json())) == test_users[offset : offset + limit]
