from ecoindex.database.engine import db
from ecoindex.models.api import HealthResponse
from ecoindex.worker.health import is_worker_healthy
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Infra"])


@router.get(
    name="Health check",
    path="",
    description="This returns the health of the service",
)
async def health_check() -> HealthResponse:
    return HealthResponse(database=db._session.is_active, workers=is_worker_healthy())
