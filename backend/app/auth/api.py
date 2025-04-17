from __future__ import annotations

from typing import List
from uuid import UUID

from litestar import Controller, get, patch
from litestar.di import Provide

from app.auth.services.user_service import UserModel, UserService, provide_user_service
from app.core.crud import Filter, Pagination, provide_pagination, provide_search_params


class UserController(Controller):
    path = "/api/users"

    dependencies = {
        "user_service": Provide(provide_user_service),
        "pagination": Provide(provide_pagination),
        "search_params": Provide(provide_search_params),
    }

    @get(path="/")
    async def get_list(
        self, user_service: UserService, pagination: Pagination, search_params: List[Filter]
    ) -> List[UserModel]:
        return await user_service.get_users(pagination, search_params)

    @patch(path="/{detail_id:str}")
    async def update(
        self,
        detail_id: UUID,
        data: UserModel,
        user_service: UserService,
    ) -> UserModel:
        return await user_service.update_detail(detail_id, data)
