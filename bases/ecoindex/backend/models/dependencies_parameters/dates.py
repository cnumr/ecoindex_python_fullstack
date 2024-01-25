from typing import Annotated

from ecoindex.backend.dependencies.dates import get_date_parameters
from ecoindex.backend.models.parameters import DateRange
from fastapi import Depends

DateRangeParameters = Annotated[DateRange, Depends(get_date_parameters)]
