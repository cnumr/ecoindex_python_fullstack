from datetime import date

from pydantic import BaseModel


class Pagination(BaseModel):
    page: int = 1
    size: int = 50


class DateRange(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
