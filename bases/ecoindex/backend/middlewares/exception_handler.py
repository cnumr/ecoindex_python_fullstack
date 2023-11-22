from ecoindex.backend.utils import format_exception_response
from ecoindex.database.exceptions.quota import QuotaExceededException
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

HTTP_520_ECOINDEX_TYPE_ERROR = 520
HTTP_521_ECOINDEX_CONNECTION_ERROR = 521


def handle_exceptions(app: FastAPI):
    @app.exception_handler(RuntimeError)
    async def handle_screenshot_not_found_exception(_: Request, exc: FileNotFoundError):
        return JSONResponse(
            content={"detail": str(exc)},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    @app.exception_handler(TypeError)
    async def handle_resource_type_error(_: Request, exc: TypeError):
        return JSONResponse(
            content={"detail": exc.args[0]},
            status_code=HTTP_520_ECOINDEX_TYPE_ERROR,
        )

    @app.exception_handler(ConnectionError)
    async def handle_connection_error(_: Request, exc: ConnectionError):
        return JSONResponse(
            content={"detail": exc.args[0]},
            status_code=HTTP_521_ECOINDEX_CONNECTION_ERROR,
        )

    @app.exception_handler(QuotaExceededException)
    async def handle_quota_exceeded_exception(_: Request, exc: QuotaExceededException):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": exc.__dict__},
        )

    @app.exception_handler(Exception)
    async def handle_exception(_: Request, exc: Exception):
        exception_response = await format_exception_response(exception=exc)
        return JSONResponse(
            content={"detail": exception_response.model_dump()},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
