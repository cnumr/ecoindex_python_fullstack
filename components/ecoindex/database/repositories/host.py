from datetime import date

from ecoindex.database.helper import date_filter
from ecoindex.database.models import ApiEcoindex
from ecoindex.models.enums import Version
from sqlalchemy import text
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_host_list_db(
    session: AsyncSession,
    version: Version = Version.v1,
    host: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    page: int = 1,
    size: int = 50,
) -> list[str]:
    statement = (
        select(ApiEcoindex.host)
        .where(ApiEcoindex.version == version.get_version_number())
        .offset(size * (page - 1))
        .limit(size)
    )

    if host:
        statement = statement.filter(ApiEcoindex.host.like(f"%{host}%"))  # type: ignore

    statement = date_filter(statement=statement, date_from=date_from, date_to=date_to)

    statement = statement.group_by(ApiEcoindex.host).order_by(ApiEcoindex.host)

    hosts = await session.exec(statement=statement)

    return [str(host) for host in hosts.all()]


async def get_count_hosts_db(
    session: AsyncSession,
    version: Version = Version.v1,
    name: str | None = None,
    q: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    group_by_host: bool = True,
) -> int:
    sub_statement = (
        f"SELECT host FROM apiecoindex WHERE version = {version.get_version_number()}"
    )
    if name:
        sub_statement += f" AND host = '{name}'"

    if q:
        sub_statement += f" AND host LIKE '%{q}%'"

    if date_from:
        sub_statement += f" AND date >= '{date_from}'"

    if date_to:
        sub_statement += f" AND date <= '{date_to}'"

    if group_by_host:
        sub_statement += " GROUP BY host"

    statement = f"SELECT count(*) FROM ({sub_statement}) t"

    result = await session.exec(statement=text(statement))  # type: ignore

    return result.scalar_one()
