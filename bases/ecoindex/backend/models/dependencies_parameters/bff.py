from typing import Annotated

from ecoindex.backend.dependencies.bff import get_bff_parameters
from ecoindex.backend.models.parameters import BffParameters
from fastapi import Depends

BffDepParameters = Annotated[BffParameters, Depends(get_bff_parameters)]
