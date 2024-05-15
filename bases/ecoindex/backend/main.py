from ecoindex.backend import get_api_version
from ecoindex.backend.routers import router
from ecoindex.backend.services.cache import cache
from ecoindex.config import Settings
from ecoindex.database.engine import init_db
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from sentry_sdk import init as sentry_init


def init_app():
    cache.init()
    if Settings().GLITCHTIP_DSN:
        sentry_init(Settings().GLITCHTIP_DSN)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await init_db()
        yield

    app = FastAPI(
        title="Ecoindex API",
        version=get_api_version(),
        description=(
            "Ecoindex API enables you to perform ecoindex analysis of given web pages"
        ),
        lifespan=lifespan,
    )

    app.include_router(router)

    from ecoindex.backend.middlewares.cors import add_cors_middleware
    from ecoindex.backend.middlewares.exception_handler import handle_exceptions

    handle_exceptions(app)
    add_cors_middleware(app)

    return app


app = init_app()
