from ecoindex.models.api import HealthWorker, HealthWorkers
from ecoindex.worker.tasks import app


def is_worker_healthy() -> HealthWorkers:
    workers = []
    workers_ping = app.control.ping()

    for worker in workers_ping:
        for name in worker:
            workers.append(
                HealthWorker(name=name, healthy=True if "ok" in worker[name] else False)
            )

    return HealthWorkers(
        healthy=False if False in [w.healthy for w in workers] or not workers else True,
        workers=workers,
    )
