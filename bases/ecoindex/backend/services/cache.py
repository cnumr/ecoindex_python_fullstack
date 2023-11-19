import json
from hashlib import sha1

from ecoindex.config import Settings
from ecoindex.database.models import EcoindexSearchResults
from pydantic import AnyHttpUrl
from redis import Redis


class EcoindexCache:
    def __init__(self) -> None:
        self._r = None

    def init(self) -> None:
        self._r = Redis(host=Settings().REDIS_CACHE_HOST, db=2)

    def set_cache_key(self, url: AnyHttpUrl):
        cleaned_url = f"{url.host}/{url.path}"
        self.cache_key = sha1(cleaned_url.encode("utf-8")).hexdigest()

        return self

    async def get_cached_ecoindex_search_results(
        self,
    ) -> EcoindexSearchResults | None:
        ecoindex_search_results = self._r.get(name=self.cache_key)

        if ecoindex_search_results:
            return EcoindexSearchResults(**json.loads(ecoindex_search_results))

        return None

    async def set_cached_ecoindex_search_results(
        self, ecoindex_search_results: EcoindexSearchResults
    ) -> None:
        self._r.set(
            name=self.cache_key,
            value=ecoindex_search_results.model_dump_json(),
            ex=60 * 60 * 24 * 7,  # set default expiration to 7 days
        )


cache = EcoindexCache()
