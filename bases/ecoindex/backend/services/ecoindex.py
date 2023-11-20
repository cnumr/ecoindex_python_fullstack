import json

from ecoindex.backend.services.cache import cache
from ecoindex.database.models import EcoindexSearchResults
from ecoindex.database.repositories.ecoindex import get_ecoindex_result_list_db
from ecoindex.models.enums import Version
from ecoindex.models.sort import Sort
from pydantic import AnyHttpUrl
from requests import get


async def get_latest_result_by_url(
    url: AnyHttpUrl, refresh: bool, version: Version
) -> EcoindexSearchResults:
    ecoindex_cache = cache.set_cache_key(key=f"ecoindex-{url.host}/{url.path}")
    cached_results = await ecoindex_cache.get()

    if not refresh and cached_results:
        return EcoindexSearchResults(**json.loads(cached_results))

    ecoindexes = await get_ecoindex_result_list_db(
        host=str(url.host),
        version=version,
        size=20,
        sort_params=[Sort(clause="date", sort="desc")],
    )

    if not ecoindexes:
        await ecoindex_cache.set_cached_ecoindex_search_results(
            ecoindex_search_results=EcoindexSearchResults(count=0).model_dump_json()
        )

        return EcoindexSearchResults(count=0)

    exact_url_results = []
    host_results = []

    for ecoindex in ecoindexes:
        if ecoindex.get_url_path() == str(url.path):
            exact_url_results.append(ecoindex)
        else:
            host_results.append(ecoindex)

    results = EcoindexSearchResults(
        count=len(exact_url_results),
        latest_result=exact_url_results[0] if exact_url_results else None,
        older_results=exact_url_results[1:] if len(exact_url_results) > 1 else [],
        host_results=host_results,
    )

    await ecoindex_cache.set(
        data=results.model_dump_json(),
    )

    return results


async def get_badge(
    url: AnyHttpUrl, refresh: bool, version: Version, theme: str
) -> str:
    results = await get_latest_result_by_url(url=url, refresh=refresh, version=version)

    grade = results.latest_result.grade if results.count > 0 else "unknown"
    ecoindex_cache = cache.set_cache_key(key=f"badge-{grade}-{theme}")

    cached_badge = await ecoindex_cache.get()

    if cached_badge:
        return cached_badge

    base_url = f"https://cdn.jsdelivr.net/gh/cnumr/ecoindex_badge@1/assets/svg/{theme}/{grade}.svg"

    image = get(base_url).text

    await ecoindex_cache.set(data=image)

    return image
