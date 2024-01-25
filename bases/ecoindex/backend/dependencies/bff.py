from typing import Annotated

from ecoindex.backend.models.dependencies_parameters.version import VersionParameter
from ecoindex.backend.models.parameters import BffParameters
from ecoindex.models.enums import Version
from fastapi import Query
from pydantic import AnyHttpUrl


def get_bff_parameters(
    url: Annotated[AnyHttpUrl, Query(description="Url to be searched in database")],
    refresh: Annotated[
        bool,
        Query(
            description="Force the refresh of the cache",
        ),
    ] = False,
    version: VersionParameter = Version.v1,
) -> BffParameters:
    return BffParameters(
        url=url,
        refresh=refresh,
        version=version,
    )
