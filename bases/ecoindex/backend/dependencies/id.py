from typing import Annotated
from uuid import UUID

from fastapi import Path


def get_id_parameter(
    id: Annotated[
        UUID,
        Path(default=..., description="Unique identifier of the ecoindex analysis"),
    ]
) -> UUID:
    return id
