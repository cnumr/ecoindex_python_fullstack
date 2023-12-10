from ecoindex.database.engine import get_session
from ecoindex.models.api import HealthResponse
from ecoindex.worker.health import is_worker_healthy
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix="/health", tags=["Infra"])


@router.get(
    name="Health check",
    path="",
    description="This returns the health of the service",
)
async def health_check(session: AsyncSession = Depends(get_session)) -> HealthResponse:
    return HealthResponse(database=session.is_active, workers=is_worker_healthy())
