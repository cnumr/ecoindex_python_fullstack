from typing import Annotated

from ecoindex.backend.dependencies import compute_parameters
from ecoindex.compute.ecoindex import compute_ecoindex
from ecoindex.models.compute import Ecoindex
from ecoindex.models.parameters import ComputeParameters
from fastapi import APIRouter, Depends

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
    parameters: Annotated[ComputeParameters, Depends(compute_parameters)]
) -> Ecoindex:
    return await compute_ecoindex(
        nodes=parameters.dom, size=parameters.size, requests=parameters.requests
    )
