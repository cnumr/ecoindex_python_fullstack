from typing import Any

from pydantic import BaseModel, Field


class ApiHealth(BaseModel):
    database: bool = Field(default=..., title="Status of database")


class BaseHost(BaseModel):
    name: str
    total_count: int


class Host(BaseHost):
    remaining_daily_requests: int | None = None


class PageHosts(BaseModel):
    items: list[str]
    total: int
    page: int
    size: int


class ExceptionResponse(BaseModel):
    args: list[Any]
    exception: str
    message: str | None = None


class HealthWorker(BaseModel):
    name: str = Field(default=..., title="Name of worker")
    healthy: bool = Field(default=..., title="Status of worker")


class HealthWorkers(BaseModel):
    healthy: bool = Field(default=..., title="Global status of workers")
    workers: list[HealthWorker] = Field(default=..., title="List of workers")


class HealthResponse(BaseModel):
    database: bool = Field(default=..., title="Status of database")
    workers: HealthWorkers = Field(default=..., title="Status of workers")
