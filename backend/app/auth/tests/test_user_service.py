from typing import List

from app.auth.services.user_service import UserModel, UserService
from app.database import Database


async def test_create_user(user_service: UserService) -> None:
    user = UserModel(
        email="superuser@mail.com",
        first_name="super",
        last_name="man",
        password="superPassword",
    )
    created_user = await user_service.create_detail(user)
    assert created_user.email == user.email

    # tear down user
    await user_service.delete_user(created_user.id)


async def test_delete_user(test_user, user_service: UserService):
    await user_service.delete_user(test_user.id)
    assert await user_service.get_user(test_user.id) is None


async def test_paginate_users(test_users: List[UserModel], db: Database) -> None:
    assert len(test_users) == 500


async def test_update_user(test_user: UserModel, user_service: UserService):
    updated_email = "updated_email@gmail.com"
    updated_user = await user_service.update_detail(test_user.id, UserModel(email=updated_email))
    assert (await user_service.get_user(updated_user.id)).email == updated_email
