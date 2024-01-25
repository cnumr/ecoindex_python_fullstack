from typing import Annotated

from ecoindex.backend.dependencies.version import get_version_parameter
from ecoindex.models.enums import Version
from fastapi import Depends

VersionParameter = Annotated[Version, Depends(get_version_parameter)]
