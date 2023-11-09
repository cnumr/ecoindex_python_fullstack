from typing import Annotated

from ecoindex.compute.ecoindex import compute_ecoindex
from ecoindex.models.compute import Ecoindex
from fastapi import APIRouter, Query

router = APIRouter(prefix="/ecoindex", tags=["Ecoindex"])


@router.get(
    name="Compute ecoindex",
    path="/ecoindex",
    tags=["Ecoindex"],
    description=(
        "This returns the ecoindex computed based on the given parameters: "
        "DOM (number of DOM nodes), size (total size in Kb) and requests"
    ),
)
async def compute_ecoindex_api(
    dom: Annotated[
        int,
        Query(
            default=...,
            description="Number of DOM nodes of the page",
            gt=0,
            example=204,
        ),
    ],
    size: Annotated[
        float,
        Query(
            default=..., description="Total size of the page in Kb", gt=0, example=109
        ),
    ],
    requests: Annotated[
        int,
        Query(
            default=..., description="Number of requests of the page", gt=0, example=5
        ),
    ],
) -> Ecoindex:
    return await compute_ecoindex(nodes=dom, size=size, requests=requests)
