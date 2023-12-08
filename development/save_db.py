from asyncio import run
from uuid import UUID, uuid4

from ecoindex.database.engine import db
from ecoindex.database.models import ApiEcoindex
from ecoindex.database.repositories.ecoindex import (
    get_count_analysis_db,
    get_rank_analysis_db,
)
from ecoindex.models.compute import Result
from ecoindex.models.enums import Version

db.init()


async def save_ecoindex_result_db(
    id: UUID,
    ecoindex_result: Result,
    version: Version = Version.v1,
) -> ApiEcoindex:
    ranking = await get_rank_analysis_db(ecoindex=ecoindex_result, version=version)
    total_results = await get_count_analysis_db(version=version)

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

    db.add(db_ecoindex)
    try:
        await db.commit()
        await db.refresh(db_ecoindex)
    except Exception:
        await db.rollback()
        raise

    return db_ecoindex


if __name__ == "__main__":
    ecoindex_db = run(
        save_ecoindex_result_db(
            id=uuid4(),
            ecoindex_result=Result(
                date="2021-09-01T00:00:00+00:00",
                url="https://www.ecoindex.fr",
                ecoindex_version="1.0.0",
                ges=0.0,
                grade="A",
                height=1080,
                nodes=0,
                page_type="home",
                requests=0,
                score=100,
                size=0,
                water=0,
                width=1920,
            ),
            version=Version.v1,
        )
    )

    print(ecoindex_db)
    run(db.close())
