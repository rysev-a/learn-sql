from uuid import UUID
from app.database import Database
from pydantic import BaseModel


class UserModel(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    password: str


async def test_create_user(db: Database) -> None:
    raw_user = await db.fetch(
        "insert into users (email, first_name, last_name, password) values ($1, $2, $3, $4) returning id",
        "superuser@mail.com",
        "super",
        "man",
        "superPassword",
    )
    user = UserModel(**await db.fetch_row("select * from users where id = $1", raw_user[0].get('id')))
    assert user.email == "superuser@mail.com"


async def test_remove_user(db: Database) -> None:
    raw_user = await db.fetch(
        "insert into users (email, first_name, last_name, password) values ($1, $2, $3, $4) returning id",
        "superuser@mail.com",
        "super",
        "man",
        "superPassword",
    )
    await db.fetch("delete from users where id = $1", raw_user[0].get('id'))
    user = await db.fetch_row("select * from users where id = $1", raw_user[0].get('id'))
    assert user is None
