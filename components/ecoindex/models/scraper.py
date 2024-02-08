from pydantic import BaseModel


class RequestItem(BaseModel):
    category: str
    mime_type: str
    size: float
    status: int
    url: str


class MimetypeMetrics(BaseModel):
    total_count: int = 0
    total_size: float = 0


class MimetypeAggregation(BaseModel):
    css: MimetypeMetrics = MimetypeMetrics()
    font: MimetypeMetrics = MimetypeMetrics()
    image: MimetypeMetrics = MimetypeMetrics()
    javascript: MimetypeMetrics = MimetypeMetrics()
    other: MimetypeMetrics = MimetypeMetrics()
    video: MimetypeMetrics = MimetypeMetrics()


class Requests(BaseModel):
    aggregation: MimetypeAggregation = MimetypeAggregation()
    items: list[RequestItem] = []
    total_count: int = 0
    total_size: float = 0
