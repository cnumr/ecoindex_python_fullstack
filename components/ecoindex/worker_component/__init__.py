from celery import Celery
from ecoindex.config.settings import Settings

app: Celery = Celery(
    "tasks",
    broker=f"redis://{Settings().REDIS_CACHE_HOST}:6379/0",
    backend=f"redis://{Settings().REDIS_CACHE_HOST}:6379/1",
    broker_connection_retry=False,
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=10,
)
