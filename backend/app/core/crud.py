from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, List, Optional

from litestar.params import Parameter


@dataclass
class Pagination:
    limit: Optional[int] = None
    offset: Optional[int] = None


@dataclass
class Filter:
    key: str
    value: str | int


async def provide_pagination(
    limit: int | None = Parameter(default=None),
    offset: int | None = Parameter(default=None),
) -> Pagination:
    return Pagination(limit, offset)


async def provide_search_params(filters: Any) -> List[Filter]:
    return [Filter(**filter_config) for filter_config in json.loads(filters)]
