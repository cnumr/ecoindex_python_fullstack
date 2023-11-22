from ecoindex.config import Settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def add_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=Settings().CORS_ALLOWED_CREDENTIALS,
        allow_headers=Settings().CORS_ALLOWED_HEADERS,
        allow_methods=Settings().CORS_ALLOWED_METHODS,
        allow_origins=Settings().CORS_ALLOWED_ORIGINS,
    )
