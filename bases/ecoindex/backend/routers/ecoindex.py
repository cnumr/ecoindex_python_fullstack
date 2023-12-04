from os import getcwd
from typing import Annotated
from uuid import UUID

from ecoindex.backend.dependencies import (
    bff_parameters,
    date_parameters,
    host_parameter,
    id_parameter,
    pagination_parameters,
    version_parameter,
)
from ecoindex.backend.services.ecoindex import get_badge, get_latest_result_by_url
from ecoindex.backend.utils import get_sort_parameters, get_status_code
from ecoindex.config.settings import Settings
from ecoindex.database.models import (
    ApiEcoindex,
    EcoindexSearchResults,
    PageApiEcoindexes,
)
from ecoindex.database.repositories.ecoindex import (
    get_count_analysis_db,
    get_ecoindex_result_by_id_db,
    get_ecoindex_result_list_db,
)
from ecoindex.models.enums import BadgeTheme, Version
from ecoindex.models.parameters import BffParameters, DateRange, Pagination
from ecoindex.models.response_examples import (
    example_ecoindex_not_found,
    example_file_not_found,
)
from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException
from fastapi.params import Query
from fastapi.responses import FileResponse, RedirectResponse

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
    host: Annotated[str, Depends(host_parameter)],
    version: Annotated[Version, Depends(version_parameter)] = Version.v1,
    date_range: Annotated[DateRange, Depends(date_parameters)] = DateRange(),
    pagination: Annotated[Pagination, Depends(pagination_parameters)] = Pagination(),
    sort: Annotated[
        list[str],
        Query(
            description=(
                "You can sort results using this param with the format "
                "`sort=param1:asc&sort=param2:desc`"
            )
        ),
    ] = ["date:desc"],
) -> PageApiEcoindexes:
    ecoindexes = await get_ecoindex_result_list_db(
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
    name="Get latest results",
    path="/latest",
    response_model=EcoindexSearchResults,
    response_description="Get latest results for a given url",
    tags=["BFF"],
)
async def get_latest_results(
    response: Response,
    parameters: Annotated[BffParameters, Depends(bff_parameters)],
) -> EcoindexSearchResults:
    """
    This returns the latest results for a given url. This feature is used by the Ecoindex
    browser extension. By default, the results are cached for 7 days.

    If the url is not found in the database, the response status code will be 404.
    """
    latest_result = await get_latest_result_by_url(
        url=parameters.url, refresh=parameters.refresh, version=parameters.version
    )

    if latest_result.count == 0:
        response.status_code = status.HTTP_404_NOT_FOUND

    return latest_result


@router.get(
    name="Get badge",
    path="/latest/badge",
    response_description="Badge of the given url from [CDN V1](https://www.jsdelivr.com/package/gh/cnumr/ecoindex_badge)",
    responses={status.HTTP_404_NOT_FOUND: example_file_not_found},
    tags=["BFF"],
)
async def get_badge_enpoint(
    parameters: Annotated[BffParameters, Depends(bff_parameters)],
    theme: Annotated[
        BadgeTheme, Query(description="Theme of the badge")
    ] = BadgeTheme.light,
) -> Response:
    """
    This returns the SVG badge of the given url. This feature is used by the Ecoindex
    badge. By default, the results are cached for 7 days.

    If the url is not found in the database, it will return a badge with the grade `?`.
    """
    return Response(
        content=await get_badge(
            url=parameters.url,
            refresh=parameters.refresh,
            version=parameters.version,
            theme=theme.value,
        ),
        media_type="image/svg+xml",
    )


@router.get(
    name="Get latest results redirect",
    path="/latest/redirect",
    response_description="Redirect to the latest results for a given url",
    tags=["BFF"],
)
async def get_latest_result_redirect(
    parameters: Annotated[BffParameters, Depends(bff_parameters)],
) -> RedirectResponse:
    """
    This redirects to the latest results on the frontend website for the given url.
    This feature is used by the Ecoindex browser extension and badge.

    If the url is not found in the database, the response status code will be 404.
    """
    latest_result = await get_latest_result_by_url(
        url=parameters.url, refresh=parameters.refresh, version=parameters.version
    )

    if latest_result.count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No analysis found for {parameters.url}",
        )

    return RedirectResponse(
        url=f"{Settings().FRONTEND_BASE_URL}/resultat/?id={latest_result.latest_result.id}"
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
    id: Annotated[UUID, Depends(id_parameter)],
    version: Annotated[Version, Depends(version_parameter)] = Version.v1,
) -> ApiEcoindex:
    ecoindex = await get_ecoindex_result_by_id_db(id=id, version=version)

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
    id: Annotated[UUID, Depends(id_parameter)],
    version: Annotated[Version, Depends(version_parameter)] = Version.v1,
):
    return FileResponse(
        path=f"{getcwd()}/screenshots/{version.value}/{id}.webp",
        filename=f"{id}.webp",
        content_disposition_type="inline",
        media_type="image/webp",
    )
