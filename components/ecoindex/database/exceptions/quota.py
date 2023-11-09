from ecoindex.config import Settings
from ecoindex.database.models import ApiEcoindex


class QuotaExceededException(Exception):
    def __init__(self, limit: int, host: str, latest_result: ApiEcoindex) -> None:
        self.daily_limit_per_host = Settings().DAILY_LIMIT_PER_HOST
        self.limit = limit
        self.host = host
        self.latest_result = latest_result
        self.message = (
            "You have already reached the daily limit "
            f"of {limit} requests for host {host} today"
        )

        super().__init__(self.message)
