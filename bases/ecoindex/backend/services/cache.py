from hashlib import sha1

from ecoindex.config import Settings
from redis import Redis


class EcoindexCache:
    def init(self) -> None:
        self._r = Redis(host=Settings().REDIS_CACHE_HOST, db=2)

    def set_cache_key(self, key: str):
        self.cache_key = sha1(key.encode("utf-8")).hexdigest()

        return self

    async def get(
        self,
    ) -> str | None:
        results = self._r.get(name=self.cache_key)

        if results:
            return results.decode("utf-8")

        return None

    async def set(self, data: str) -> None:
        self._r.set(
            name=self.cache_key,
            value=data,
            ex=60 * 60 * 24 * 7,  # set default expiration to 7 days
        )


cache = EcoindexCache()
