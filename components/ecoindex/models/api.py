from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from ecoindex.models.compute import Result


class ApiEcoindex(Result):
    id: UUID | None = Field(
        default=None,
        description="Analysis ID of type `UUID`",
    )
    host: str = Field(
        default=...,
        title="Web page host",
        description="Host name of the web page",
    )
    version: int = Field(
        default=1,
        title="API version",
        description="Version number of the API used to run the test",
    )
    initial_ranking: int | None = Field(
        default=...,
        title="Analysis rank",
        description=(
            "This is the initial rank of the analysis. "
            "This is an indicator of the ranking at the "
            "time of the analysis for a given version."
        ),
    )
    initial_total_results: int | None = Field(
        default=...,
        title="Total number of analysis",
        description=(
            "This is the initial total number of analysis. "
            "This is an indicator of the total number of analysis "
            "at the time of the analysis for a given version."
        ),
    )


class PageApiEcoindexes(BaseModel):
    items: List[ApiEcoindex]
    total: int
    page: int
    size: int


class ApiHealth(BaseModel):
    database: bool = Field(default=..., title="Status of database")


class BaseHost(BaseModel):
    name: str
    total_count: int


class Host(BaseHost):
    remaining_daily_requests: int | None


class PageHosts(BaseModel):
    items: List[str]
    total: int
    page: int
    size: int
