from typing import Annotated

from ecoindex.backend.dependencies.pagination import get_pagination_parameters
from ecoindex.backend.models.parameters import Pagination
from fastapi import Depends

PaginationParameters = Annotated[Pagination, Depends(get_pagination_parameters)]
