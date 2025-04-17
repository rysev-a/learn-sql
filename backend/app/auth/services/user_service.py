from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.core.crud import Filter, Pagination
from app.database import Database


class UserModel(BaseModel):
    id: Optional[UUID] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    birthdate: Optional[date] = None


class UserService:
    def __init__(self, database: Database) -> None:
        self.db = database

    async def get_users(
        self,
        pagination: Optional[Pagination] = None,
        search_params: List[Filter] = None,
    ) -> List[UserModel]:
        sql_query = "SELECT * FROM users"
        sql_query = self._apply_filtration(sql_query, search_params)
        sql_query = self._apply_pagination(sql_query, pagination)

        print(sql_query)

        return [UserModel(**user) for user in await self.db.fetch(sql_query)]

    async def remove_users(self):
        await self.db.fetch("DELETE FROM users")

    async def get_user(self, detail_id: UUID) -> Optional[UserModel]:
        db_user = await self.db.fetch_row("SELECT * FROM users WHERE id=$1", detail_id)
        if not db_user:
            return None
        return UserModel(**db_user)

    async def insert_users(self, users: List[UserModel]):
        await self.db.execute_many(
            """insert into users(email, first_name, last_name, password) values($1, $2, $3, $4)""",
            [(user.email, user.first_name, user.last_name, user.password) for user in users],
        )

    async def delete_user(self, detail_id: UUID):
        await self.db.fetch("delete from users where id=$1", detail_id)

    async def update_detail(self, detail_id: UUID, data: UserModel):
        data = data.model_dump(exclude_unset=True)
        fields = [key for key in data.keys() if key != "id"]
        values = [data.get(key) for key in fields]
        mask = ", ".join([f"{key}=${str(index + 2)}" for index, key in enumerate(fields)])
        sql_query_template = f"UPDATE users SET {mask} where id=$1 returning *"
        return UserModel(**await self.db.fetch_row(sql_query_template, detail_id, *values))

    async def create_detail(self, data: UserModel):
        data = data.model_dump(exclude_unset=True)
        fields = [key for key in data.keys() if key != "id"]
        values = [data.get(key) for key in fields]
        fields_mask = ", ".join(fields)
        mask = ", ".join([f"${index + 1}" for index in range(0, len(fields))])
        sql_query_template = f"INSERT INTO users ({fields_mask}) VALUES ({mask}) returning *"
        return UserModel(**await self.db.fetch_row(sql_query_template, *values))

    @staticmethod
    def _apply_pagination(sql_query: str, pagination: Pagination) -> str:
        sql_query_with_pagination = sql_query
        if pagination:
            if pagination.limit:
                sql_query_with_pagination = sql_query_with_pagination + f"\nLIMIT {pagination.limit}"
            if pagination.offset:
                sql_query_with_pagination = sql_query_with_pagination + f"\nOFFSET {pagination.offset}"

        return sql_query_with_pagination


    @staticmethod
    def _apply_filtration(sql_query: str, search_params: List[Filter] = None) -> str:
        sql_query_with_filtration = sql_query
        if search_params:
            sql_query_with_filtration = sql_query_with_filtration + "\nwhere "
            for search in search_params:
                sql_query_with_filtration = sql_query_with_filtration + f"{search.key} = '{search.value}'"
        return sql_query_with_filtration

async def provide_user_service(db: Database) -> UserService:
    return UserService(db)
