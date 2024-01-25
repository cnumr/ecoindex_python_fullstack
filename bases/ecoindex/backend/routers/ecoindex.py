from os import getcwd
from typing import Annotated

from ecoindex.backend.models.dependencies_parameters.dates import DateRangeParameters
from ecoindex.backend.models.dependencies_parameters.host import HostParameter
from ecoindex.backend.models.dependencies_parameters.id import IdParameter
from ecoindex.backend.models.dependencies_parameters.pagination import (
    PaginationParameters,
)
from ecoindex.backend.models.dependencies_parameters.version import VersionParameter
from ecoindex.backend.models.parameters import DateRange, Pagination
from ecoindex.backend.utils import get_sort_parameters, get_status_code
from ecoindex.database.engine import get_session
from ecoindex.database.models import (
    ApiEcoindex,
    PageApiEcoindexes,
)
from ecoindex.database.repositories.ecoindex import (
    get_count_analysis_db,
    get_ecoindex_result_by_id_db,
    get_ecoindex_result_list_db,
)
from ecoindex.models import example_ecoindex_not_found, example_file_not_found
from ecoindex.models.enums import Version
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.params import Query
from fastapi.responses import FileResponse
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix="/{version}/ecoindexes", tags=["Ecoindex"])


@router.get(
    name="Get ecoindex analysis list",
    path="",
    response_model=PageApiEcoindexes,
    response_description="List of corresponding ecoindex results",
    responses={
        status.HTTP_206_PARTIAL_CONTENT: {"model": PageApiEcoindexes},
        status.HTTP_404_NOT_FOUND: {"model": PageApiEcoindexes},
    },
    description=(
        "This returns a list of ecoindex analysis "
        "corresponding to query filters and the given version engine. "
        "The results are ordered by ascending date"
    ),
)
async def get_ecoindex_analysis_list(
    response: Response,
    host: HostParameter,
    version: VersionParameter = Version.v1,
    date_range: DateRangeParameters = DateRange(),
    pagination: PaginationParameters = Pagination(),
    sort: Annotated[
        list[str],
        Query(
            description=(
                "You can sort results using this param with the format "
                "`sort=param1:asc&sort=param2:desc`"
            )
        ),
    ] = ["date:desc"],
    session: AsyncSession = Depends(get_session),
) -> PageApiEcoindexes:
    ecoindexes = await get_ecoindex_result_list_db(
        session=session,
        date_from=date_range.date_from,
        date_to=date_range.date_to,
        host=host,
        version=version,
        page=pagination.page,
        size=pagination.size,
        sort_params=await get_sort_parameters(
            query_params=sort, model=ApiEcoindex
        ),  # type: ignore
    )
    total_results = await get_count_analysis_db(
        session=session,
        version=version,
        date_from=date_range.date_from,
        date_to=date_range.date_to,
        host=host,
    )

    response.status_code = await get_status_code(items=ecoindexes, total=total_results)

    return PageApiEcoindexes(
        items=ecoindexes,
        total=total_results,
        page=pagination.page,
        size=pagination.size,
    )


@router.get(
    name="Get ecoindex analysis by id",
    path="/{id}",
    response_model=ApiEcoindex,
    response_description="Get one ecoindex result by its id",
    responses={status.HTTP_404_NOT_FOUND: example_ecoindex_not_found},
    description="This returns an ecoindex given by its unique identifier",
)
async def get_ecoindex_analysis_by_id(
    id: IdParameter,
    version: VersionParameter = Version.v1,
    session: AsyncSession = Depends(get_session),
) -> ApiEcoindex:
    ecoindex = await get_ecoindex_result_by_id_db(
        session=session, id=id, version=version
    )

    if not ecoindex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {id} not found for version {version.value}",
        )
    return ecoindex


@router.get(
    name="Get screenshot",
    path="/{id}/screenshot",
    description="This returns the screenshot of the webpage analysis if it exists",
    responses={status.HTTP_404_NOT_FOUND: example_file_not_found},
)
async def get_screenshot_endpoint(
    id: IdParameter,
    version: VersionParameter = Version.v1,
):
    return FileResponse(
        path=f"{getcwd()}/screenshots/{version.value}/{id}.webp",
        filename=f"{id}.webp",
        content_disposition_type="inline",
        media_type="image/webp",
    )
