from typing import Any
from uuid import UUID

from app.database import Database


class Service:
    def __init__(self, table: str, db: Database):
        self.table = table
        self.db = db

    async def get_list(self):
        return await self.db.fetch(f"SELECT * FROM {self.table}")

    async def get_detail(self, detail_id: UUID):
        return await self.db.fetch(f"SELECT * FROM {self.table} WHERE id={detail_id}")

    async def remove_detail(self, detail_id: UUID):
        return await self.db.fetch(f"DELETE FROM {self.table} WHERE id={detail_id}")

    async def create_detail(self, data: dict[str, Any]):
        fields = ", ".join(data.keys())
        mask = ", ".join([f"${index + 1}" for index in range(0, len(data))])
        sql_query_template = f"INSERT INTO {self.table} ({fields}) VALUES ({mask}) returning id"
        return await self.db.fetch(sql_query_template, *data.values())

    async def update_detail(self, detail_id: UUID, data: dict[str, Any]):
        mask = ", ".join([f"{key}=${str(index+2)}" for index, key in enumerate(data.keys())])
        sql_query_template = f"UPDATE {self.table} SET {mask} where id=$1 returning id"
        return await self.db.fetch(sql_query_template, detail_id, *data.values())
