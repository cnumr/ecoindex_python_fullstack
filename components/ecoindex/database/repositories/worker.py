from uuid import UUID

from ecoindex.database.models import ApiEcoindex
from ecoindex.database.repositories.ecoindex import (
    get_count_analysis_db,
    get_rank_analysis_db,
)
from ecoindex.models import Result
from ecoindex.models.enums import Version
from sqlmodel.ext.asyncio.session import AsyncSession


async def save_ecoindex_result_db(
    session: AsyncSession,
    id: UUID,
    ecoindex_result: Result,
    version: Version = Version.v1,
) -> ApiEcoindex:
    ranking = await get_rank_analysis_db(
        session=session, ecoindex=ecoindex_result, version=version
    )
    total_results = await get_count_analysis_db(session=session, version=version)

    db_ecoindex = ApiEcoindex(
        id=id,
        date=ecoindex_result.date,
        url=ecoindex_result.url,
        host=ecoindex_result.get_url_host(),
        width=ecoindex_result.width,
        height=ecoindex_result.height,
        size=ecoindex_result.size,
        nodes=ecoindex_result.nodes,
        requests=ecoindex_result.requests,
        grade=ecoindex_result.grade,
        score=ecoindex_result.score,
        ges=ecoindex_result.ges,
        water=ecoindex_result.water,
        page_type=ecoindex_result.page_type,
        version=version.get_version_number(),
        initial_ranking=ranking if ranking else total_results + 1,
        initial_total_results=total_results + 1,
        ecoindex_version=ecoindex_result.ecoindex_version,
    )

    session.add(db_ecoindex)
    try:
        await session.commit()
        await session.refresh(db_ecoindex)
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

    return db_ecoindex
