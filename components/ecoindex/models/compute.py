import os
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Any

from ecoindex.models.enums import Grade
from pydantic import AnyHttpUrl, BaseModel, Field, field_validator

PageType = str


@lru_cache
def get_compute_version() -> str:
    current_directory = os.path.dirname(os.path.realpath(__file__))
    version_filename = os.path.join(current_directory, "..", "compute", "VERSION")

    with open(version_filename, "r") as f:
        return (f.read()).strip()


class Ecoindex(BaseModel):
    grade: Grade | None = Field(
        default=None,
        title="Ecoindex grade",
        description="Is the corresponding ecoindex grade of the page (from A to G)",
    )
    score: float | None = Field(
        default=None,
        title="Ecoindex score",
        description="Is the corresponding ecoindex score of the page (0 to 100)",
        ge=0,
        le=100,
    )
    ges: float | None = Field(
        default=None,
        title="Ecoindex GES equivalent",
        description=(
            "Is the equivalent of greenhouse gases emission" " (in `gCO2e`) of the page"
        ),
        ge=0,
    )
    water: float | None = Field(
        default=None,
        title="Ecoindex Water equivalent",
        description="Is the equivalent water consumption (in `cl`) of the page",
        ge=0,
    )
    ecoindex_version: str | None = Field(
        default=get_compute_version(),
        title="Ecoindex version",
        description="Is the version of the ecoindex used to compute the score",
    )


class PageMetrics(BaseModel):
    size: float = Field(
        default=...,
        title="Page size",
        description=(
            "Is the size of the page and of the downloaded"
            " elements of the page in KB"
        ),
        ge=0,
    )
    nodes: int = Field(
        default=...,
        title="Page nodes",
        description="Is the number of the DOM elements in the page",
        ge=0,
    )
    requests: int = Field(
        default=...,
        title="Page requests",
        description="Is the number of external requests made by the page",
        ge=0,
    )


class WebPage(BaseModel):
    width: int | None = Field(
        default=1920,
        title="Page Width",
        description="Width of the simulated window in pixel",
        ge=100,
        le=3840,
    )
    height: int | None = Field(
        default=1080,
        title="Page Height",
        description="Height of the simulated window in pixel",
        ge=50,
        le=2160,
    )
    url: str = Field(
        default=...,
        title="Page url",
        description="Url of the analysed page",
        examples=["https://www.ecoindex.fr"],
    )

    @field_validator("url")
    @classmethod
    def url_as_http_url(cls, v: str) -> str:
        url_object = AnyHttpUrl(url=v)
        assert url_object.scheme in {"http", "https"}, "scheme must be http or https"

        return url_object.unicode_string()

    def get_url_host(self) -> str:
        url_object = AnyHttpUrl(url=self.url)

        return str(url_object.host)

    def get_url_path(self) -> str:
        url_obect = AnyHttpUrl(url=self.url)

        return str(url_obect.path)


class WindowSize(BaseModel):
    height: int = Field(
        default=...,
        title="Window height",
        description="Height of the simulated window in pixel",
    )
    width: int = Field(
        default=...,
        title="Window width",
        description="Width of the simulated window in pixel",
    )

    def __str__(self) -> str:
        return f"{self.width},{self.height}"


class Result(Ecoindex, PageMetrics, WebPage):
    date: datetime | None = Field(
        default=None, title="Analysis datetime", description="Date of the analysis"
    )
    page_type: PageType | None = Field(
        default=None,
        title="Page type",
        description="Is the type of the page, based ton the [opengraph type tag](https://ogp.me/#types)",
    )


class ScreenShot(BaseModel):
    id: str
    folder: str

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        path = Path(__pydantic_self__.folder)
        path.mkdir(parents=True, exist_ok=True)

    def __str__(self) -> str:
        return f"{self.folder}/{self.id}"

    def get_png(self) -> str:
        return f"{self.__str__()}.png"

    def get_webp(self) -> str:
        return f"{self.__str__()}.webp"


class Request(BaseModel):
    url: str
    type: str
    size: float
