from typing import Annotated

from ecoindex.backend.dependencies.compute import get_compute_parameters
from ecoindex.backend.models.parameters import ComputeParameters
from fastapi import Depends

ComputeDepParameters = Annotated[ComputeParameters, Depends(get_compute_parameters)]
