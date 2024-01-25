from typing import Annotated

from ecoindex.backend.models.parameters import ComputeParameters
from fastapi import Query


def get_compute_parameters(
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
) -> ComputeParameters:
    return ComputeParameters(dom=dom, size=size, requests=requests)
