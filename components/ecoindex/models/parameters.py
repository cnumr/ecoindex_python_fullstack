from datetime import date

from ecoindex.models.enums import Version
from pydantic import AnyHttpUrl, BaseModel


class Pagination(BaseModel):
    page: int = 1
    size: int = 50


class DateRange(BaseModel):
    date_from: date | None = None
    date_to: date | None = None


class BffParameters(BaseModel):
    url: AnyHttpUrl
    refresh: bool = False
    version: Version = Version.v1
