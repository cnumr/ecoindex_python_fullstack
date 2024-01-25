from ecoindex.backend.models.dependencies_parameters.compute import ComputeDepParameters
from ecoindex.compute.ecoindex import compute_ecoindex
from ecoindex.models.compute import Ecoindex
from fastapi import APIRouter

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
async def compute_ecoindex_api(parameters: ComputeDepParameters) -> Ecoindex:
    return await compute_ecoindex(
        nodes=parameters.dom, size=parameters.size, requests=parameters.requests
    )
