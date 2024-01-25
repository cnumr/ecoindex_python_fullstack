from typing import Annotated

from ecoindex.backend.dependencies.host import get_host_parameter
from fastapi import Depends

HostParameter = Annotated[str | None, Depends(get_host_parameter)]
