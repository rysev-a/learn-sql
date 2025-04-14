from dataclasses import dataclass

import click
import yaml

from lab.core.cli import coro

from app.database import database
from app.settings import APP_PATH, settings


@dataclass
class UserData:
    email: str
    first_name: str
    last_name: str
    password: str


async def init_database():
    await database.connect(settings.db_uri, settings.pool_db)


@click.group()
def auth_cli(): ...


@auth_cli.command()
@coro
async def load_users():
    await init_database()
    await database.fetch("delete from roles")
    await database.fetch("delete from users")

    users = []
    with open(f"{APP_PATH}/fixtures/users.yaml", "r") as f:
        for user_raw in yaml.safe_load(f):
            user = UserData(**user_raw)
            users.append(user)

    await database.execute_many(
        """insert into users(email, first_name, last_name, password) values($1, $2, $3, $4)""",
        [(user.email, user.first_name, user.last_name, user.password) for user in users],
    )
