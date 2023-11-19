from ecoindex.backend.routers import router
from ecoindex.backend.services.cache import cache
from ecoindex.database import db
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager


def init_app():
    db.init()
    cache.init()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await db.create_all()
        yield
        await db._session.close()

    app = FastAPI(
        title="Ecoindex API",
        version="1.0.0",
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
