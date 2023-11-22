from datetime import date
from typing import Annotated
from uuid import UUID

from ecoindex.models.enums import Version
from ecoindex.models.parameters import (
    BffParameters,
    ComputeParameters,
    DateRange,
    Pagination,
)
from fastapi import Depends, Path, Query
from pydantic import AnyHttpUrl


def date_parameters(
    date_from: Annotated[
        date | None,
        Query(description="Start date of the filter elements (example: 2020-01-01)"),
    ] = None,
    date_to: Annotated[
        date | None,
        Query(description="End date of the filter elements  (example: 2020-01-01)"),
    ] = None,
) -> DateRange:
    return DateRange(date_from=date_from, date_to=date_to)


def pagination_parameters(
    page: Annotated[int, Query(description="Page number", ge=1)] = 1,
    size: Annotated[
        int, Query(description="Number of elements per page", ge=1, le=100)
    ] = 50,
) -> Pagination:
    return Pagination(page=page, size=size)


def version_parameter(
    version: Version = Path(
        default=...,
        title="Engine version",
        description="Engine version used to run the analysis (v0 or v1)",
        example=Version.v1.value,
    )
) -> Version:
    return version


def host_parameter(
    host: Annotated[
        str | None, Query(description="Host name you want to filter (can be partial)")
    ] = None,
) -> str | None:
    return host


def id_parameter(
    id: Annotated[
        UUID,
        Path(default=..., description="Unique identifier of the ecoindex analysis"),
    ]
) -> UUID:
    return id


def bff_parameters(
    url: Annotated[AnyHttpUrl, Query(description="Url to be searched in database")],
    refresh: Annotated[
        bool,
        Query(
            description="Force the refresh of the cache",
        ),
    ] = False,
    version: Annotated[Version, Depends(version_parameter)] = Version.v1,
) -> BffParameters:
    return BffParameters(
        url=url,
        refresh=refresh,
        version=version,
    )


def compute_parameters(
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
