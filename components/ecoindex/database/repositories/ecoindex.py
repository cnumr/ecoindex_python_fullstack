from datetime import date
from uuid import UUID

from ecoindex.database.engine import db
from ecoindex.database.helper import date_filter
from ecoindex.database.models import ApiEcoindex
from ecoindex.models import Result
from ecoindex.models.enums import Version
from ecoindex.models.sort import Sort
from sqlalchemy import func, text
from sqlalchemy.sql.expression import asc, desc
from sqlmodel import select


async def get_count_analysis_db(
    version: Version | None = Version.v1,
    host: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
) -> int:
    statement = (
        "SELECT count(*) FROM apiecoindex "
        f"WHERE version = {version.get_version_number()}"
    )

    if host:
        statement += f" AND host = '{host}'"

    if date_from:
        statement += f" AND date >= '{date_from}'"

    if date_to:
        statement += f" AND date <= '{date_to}'"

    result = await db.execute(statement=text(statement))

    return result.scalar()


async def get_rank_analysis_db(
    ecoindex: Result, version: Version | None = Version.v1
) -> int | None:
    statement = (
        "SELECT ranking FROM ("
        "SELECT *, ROW_NUMBER() OVER (ORDER BY score DESC) ranking "
        "FROM apiecoindex "
        f"WHERE version={version.get_version_number()} "
        "ORDER BY score DESC) t "
        f"WHERE score <= {ecoindex.score} "
        "LIMIT 1;"
    )

    result = await db.execute(text(statement))

    return result.scalar()


async def get_ecoindex_result_list_db(
    version: Version | None = Version.v1,
    host: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    page: int | None = 1,
    size: int | None = 50,
    sort_params: list[Sort] = [],
) -> list[ApiEcoindex]:
    statement = (
        select(ApiEcoindex)
        .where(ApiEcoindex.version == version.get_version_number())
        .offset((page - 1) * size)
        .limit(size)
    )

    if host:
        statement = statement.where(ApiEcoindex.host == host)
    statement = date_filter(statement=statement, date_from=date_from, date_to=date_to)

    for sort in sort_params:
        if sort.sort == "asc":
            sort_parameter = asc(sort.clause)
        elif sort.sort == "desc":
            sort_parameter = desc(sort.clause)

        statement = statement.order_by(sort_parameter)

    ecoindexes = await db.execute(statement)

    return ecoindexes.scalars().all()


async def get_ecoindex_result_by_id_db(
    id: UUID, version: Version | None = Version.v1
) -> ApiEcoindex:
    statement = (
        select(ApiEcoindex)
        .where(ApiEcoindex.id == id)
        .where(ApiEcoindex.version == version.get_version_number())
    )

    ecoindex = await db.execute(statement)

    return ecoindex.scalar_one_or_none()


async def get_count_daily_request_per_host(host: str) -> int:
    statement = select(ApiEcoindex).where(
        func.date(ApiEcoindex.date) == date.today(), ApiEcoindex.host == host
    )

    results = await db.execute(statement)

    return len(results.all())


async def get_latest_result(host: str) -> ApiEcoindex:
    statement = (
        select(ApiEcoindex)
        .where(ApiEcoindex.host == host)
        .order_by(desc(ApiEcoindex.date))
        .limit(1)
    )

    result = await db.execute(statement)

    print(result)

    return result.scalar_one_or_none()
