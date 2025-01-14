from typing import Annotated

from ecoindex.config.settings import Settings
from fastapi import Header, HTTPException, status


def validate_api_key_batch(
    api_key: Annotated[
        str,
        Header(alias="X-Api-Key"),
    ],
):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )

    for authorized_api_key in Settings().API_KEYS_BATCH:
        if api_key == authorized_api_key["key"]:
            return authorized_api_key

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid API key",
    )
