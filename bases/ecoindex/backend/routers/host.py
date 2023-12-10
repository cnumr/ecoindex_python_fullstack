from typing import Annotated

from ecoindex.backend.dependencies import (
    date_parameters,
    host_parameter,
    pagination_parameters,
    version_parameter,
)
from ecoindex.backend.utils import check_quota, get_status_code
from ecoindex.database.engine import get_session
from ecoindex.database.repositories.host import get_count_hosts_db, get_host_list_db
from ecoindex.models.api import Host, PageHosts
from ecoindex.models.enums import Version
from ecoindex.models.parameters import DateRange, Pagination
from ecoindex.models.response_examples import example_daily_limit_response
from fastapi import Depends, Path, status
from fastapi.param_functions import Query
from fastapi.responses import Response
from fastapi.routing import APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix="/{version}/hosts", tags=["Host"])


@router.get(
    name="Get host list",
    path="",
    response_model=PageHosts,
    response_description="List ecoindex hosts",
    responses={
        status.HTTP_206_PARTIAL_CONTENT: {"model": PageHosts},
        status.HTTP_404_NOT_FOUND: {"model": PageHosts},
    },
    description=(
        "This returns a list of hosts that "
        "ran an ecoindex analysis order by most request made"
    ),
)
async def get_host_list(
    response: Response,
    host: Annotated[str, Depends(host_parameter)],
    version: Annotated[Version, Depends(version_parameter)] = Version.v1,
    date_range: Annotated[DateRange, Depends(date_parameters)] = DateRange(),
    pagination: Annotated[Pagination, Depends(pagination_parameters)] = Pagination(),
    q: str = Query(
        default=None,
        description="Filter by partial host name (replaced by `host`)",
        deprecated=True,
    ),
    session: AsyncSession = Depends(get_session),
) -> PageHosts:
    hosts = await get_host_list_db(
        session=session,
        date_from=date_range.date_from,
        date_to=date_range.date_to,
        host=host or q,
        version=version,
        page=pagination.page,
        size=pagination.size,
    )

    total_hosts = await get_count_hosts_db(
        session=session,
        version=version,
        q=q,
        date_from=date_range.date_from,
        date_to=date_range.date_to,
    )

    response.status_code = await get_status_code(items=hosts, total=total_hosts)

    return PageHosts(
        items=hosts, total=total_hosts, page=pagination.page, size=pagination.size
    )


@router.get(
    name="Get host details",
    path="/{host}",
    response_description="Host details",
    responses={
        status.HTTP_200_OK: {"model": Host},
        status.HTTP_404_NOT_FOUND: {"model": Host},
        status.HTTP_429_TOO_MANY_REQUESTS: example_daily_limit_response,
    },
    description=(
        "This returns the details of a host. If no no quota is set, "
        "remaining_daily_requests will be null"
    ),
)
async def get_daily_remaining(
    host: Annotated[str, Path(..., description="Exact matching host name")],
    version: Annotated[Version, Depends(version_parameter)] = Version.v1,
    session: AsyncSession = Depends(get_session),
) -> Host:
    return Host(
        name=host,
        remaining_daily_requests=await check_quota(session=session, host=host),
        total_count=await get_count_hosts_db(
            session=session, name=host, version=version, group_by_host=False
        ),
    )
