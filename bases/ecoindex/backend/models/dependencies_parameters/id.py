from typing import Annotated
from uuid import UUID

from ecoindex.backend.dependencies.id import get_id_parameter
from fastapi import Depends

IdParameter = Annotated[UUID, Depends(get_id_parameter)]
