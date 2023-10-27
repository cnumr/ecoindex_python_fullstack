from pydantic import BaseModel


class RequestItem(BaseModel):
    mime_type: str
    size: float
    status: int
    url: str


class Requests(BaseModel):
    items: list[RequestItem] = []
    total_count: int = 0
    total_size: float = 0
