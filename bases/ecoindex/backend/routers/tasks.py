from json import loads

from celery.result import AsyncResult
from ecoindex.backend.models.dependencies_parameters.id import IdParameter
from ecoindex.backend.utils import check_quota
from ecoindex.config.settings import Settings
from ecoindex.database.engine import get_session
from ecoindex.models import WebPage
from ecoindex.models.enums import TaskStatus
from ecoindex.models.response_examples import example_daily_limit_response
from ecoindex.models.tasks import QueueTaskApi, QueueTaskResult
from ecoindex.worker.tasks import ecoindex_task
from ecoindex.worker_component import app as task_app
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.params import Body
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix="/v1/tasks/ecoindexes", tags=["Tasks"])


@router.post(
    name="Add new ecoindex analysis task to the waiting queue",
    path="/",
    response_description="Identifier of the task that has been created in queue",
    responses={
        status.HTTP_201_CREATED: {"model": str},
        status.HTTP_403_FORBIDDEN: {"model": str},
        status.HTTP_429_TOO_MANY_REQUESTS: example_daily_limit_response,
    },
    description="This submits a ecoindex analysis task to the engine",
    status_code=status.HTTP_201_CREATED,
)
async def add_ecoindex_analysis_task(
    response: Response,
    web_page: WebPage = Body(
        default=...,
        title="Web page to analyze defined by its url and its screen resolution",
        example=WebPage(url="https://www.ecoindex.fr", width=1920, height=1080),
    ),
    session: AsyncSession = Depends(get_session),
) -> str:
    if Settings().DAILY_LIMIT_PER_HOST:
        remaining_quota = await check_quota(
            session=session, host=web_page.get_url_host()
        )
        response.headers["X-Remaining-Daily-Requests"] = str(remaining_quota - 1)

    if (
        Settings().EXCLUDED_HOSTS
        and web_page.get_url_host() in Settings().EXCLUDED_HOSTS
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This host is excluded from the analysis",
        )

    task_result = ecoindex_task.delay(
        url=str(web_page.url), width=web_page.width, height=web_page.height
    )

    return task_result.id


@router.get(
    name="Get ecoindex analysis task by id",
    path="/{id}",
    responses={
        status.HTTP_200_OK: {"model": QueueTaskApi},
        status.HTTP_425_TOO_EARLY: {"model": QueueTaskApi},
    },
    response_description="Get one ecoindex task result by its id",
    description="This returns an ecoindex given by its unique identifier",
)
async def get_ecoindex_analysis_task_by_id(
    response: Response,
    id: IdParameter,
) -> QueueTaskApi:
    t = AsyncResult(id=str(id), app=task_app)

    task_response = QueueTaskApi(
        id=t.id,
        status=t.state,
    )

    if t.state == TaskStatus.PENDING:
        response.status_code = status.HTTP_425_TOO_EARLY

        return task_response

    if t.state == TaskStatus.SUCCESS:
        task_response.ecoindex_result = QueueTaskResult(**loads(t.result))

    if t.state == TaskStatus.FAILURE:
        task_response.task_error = t.info

    response.status_code = status.HTTP_200_OK

    return task_response


@router.delete(
    name="Abort ecoindex analysis by id",
    path="/{id}",
    response_description="Abort one ecoindex task by its id if it is still waiting",
    description="This aborts one ecoindex task by its id if it is still waiting",
)
async def delete_ecoindex_analysis_task_by_id(
    id: IdParameter,
) -> None:
    res = task_app.control.revoke(id, terminate=True, signal="SIGKILL")

    return res
