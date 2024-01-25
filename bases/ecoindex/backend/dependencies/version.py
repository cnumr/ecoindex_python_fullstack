from ecoindex.models.enums import Version
from fastapi import Path


def get_version_parameter(
    version: Version = Path(
        default=...,
        title="Engine version",
        description="Engine version used to run the analysis (v0 or v1)",
        example=Version.v1.value,
    )
) -> Version:
    return version
