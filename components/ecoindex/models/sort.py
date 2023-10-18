from typing import Literal

from pydantic import BaseModel


class Sort(BaseModel):
    clause: str
    sort: Literal["asc", "desc"]
