from typing import Annotated

from fastapi import Query


def get_host_parameter(
    host: Annotated[
        str | None, Query(description="Host name you want to filter (can be partial)")
    ] = None,
) -> str | None:
    return host
