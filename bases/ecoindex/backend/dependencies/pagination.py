from typing import Annotated

from ecoindex.backend.models.parameters import Pagination
from fastapi import Query


def get_pagination_parameters(
    page: Annotated[int, Query(description="Page number", ge=1)] = 1,
    size: Annotated[
        int, Query(description="Number of elements per page", ge=1, le=100)
    ] = 50,
) -> Pagination:
    return Pagination(page=page, size=size)
