import asyncio
from concurrent.futures import ProcessPoolExecutor
from datetime import date
import uuid

import click
from faker import Faker
import yaml

from lab.auth.auth_core import hash_password
from lab.core.cli import coro

from app.auth.services.user_service import UserModel
from app.database import Database
from app.settings import APP_PATH, settings

fake = Faker()

GENERATE_USERS_COUNT = 500


async def load_users_fixtures(database: Database):
    users = []
    with open(f"{APP_PATH}/auth/fixtures/users.yaml", "r") as f:
        for user_raw in yaml.safe_load(f):
            user = UserModel(**user_raw)
            users.append(user)

    await database.execute_many(
        """insert into users(id, email, first_name, last_name, birthdate, password) values($1, $2, $3, $4, $5, $6)""",
        [(user.id, user.email, user.first_name, user.last_name, user.birthdate, user.password) for user in users],
    )


@click.group()
def auth_cli(): ...


@auth_cli.command()
@coro
async def load_users():
    database = Database()
    await database.connect(settings.db_uri, settings.pool_db)
    await database.fetch("delete from roles")
    await database.fetch("delete from users")
    await load_users_fixtures(database)


def generate_user(email, first_name, last_name, birthdate):
    password = hash_password(first_name)

    return UserModel(
        id=uuid.uuid4(),
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
        birthdate=birthdate,
    )


@auth_cli.command()
@coro
async def generate_users():
    executor = ProcessPoolExecutor(16)
    loop = asyncio.get_event_loop()

    tasks = []
    for i in range(GENERATE_USERS_COUNT):
        email = fake.unique.email()
        first_name = fake.unique.first_name()
        last_name = fake.unique.last_name()
        birthdate = fake.date(end_datetime=date(2000, 1, 1))

        tasks.append(
            loop.run_in_executor(
                executor,
                generate_user,
                email,
                first_name,
                last_name,
                birthdate,
            )
        )
    users = await asyncio.gather(*tasks)
    with open(f"{APP_PATH}/auth/fixtures/users.yaml", "w") as f:
        users_data = [{**user.dict(), "id": str(user.id)} for user in users]
        f.write(yaml.dump(users_data))
