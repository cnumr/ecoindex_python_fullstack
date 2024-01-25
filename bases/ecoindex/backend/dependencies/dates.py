from datetime import date
from typing import Annotated

from ecoindex.backend.models.parameters import DateRange
from fastapi import Query


def get_date_parameters(
    date_from: Annotated[
        date | None,
        Query(description="Start date of the filter elements (example: 2020-01-01)"),
    ] = None,
    date_to: Annotated[
        date | None,
        Query(description="End date of the filter elements  (example: 2020-01-01)"),
    ] = None,
) -> DateRange:
    return DateRange(date_from=date_from, date_to=date_to)
