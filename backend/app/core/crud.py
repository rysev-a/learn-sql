from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from litestar.params import Parameter


@dataclass
class Pagination:
    limit: Optional[int] = None
    offset: Optional[int] = None


async def provide_pagination(
    limit: int | None = Parameter(default=None),
    offset: int | None = Parameter(default=None),
) -> Pagination:
    return Pagination(limit, offset)
