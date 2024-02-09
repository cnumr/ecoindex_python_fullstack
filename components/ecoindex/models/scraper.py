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
    audio: MimetypeMetrics = MimetypeMetrics()
    css: MimetypeMetrics = MimetypeMetrics()
    font: MimetypeMetrics = MimetypeMetrics()
    html: MimetypeMetrics = MimetypeMetrics()
    image: MimetypeMetrics = MimetypeMetrics()
    javascript: MimetypeMetrics = MimetypeMetrics()
    other: MimetypeMetrics = MimetypeMetrics()
    video: MimetypeMetrics = MimetypeMetrics()

    @classmethod
    async def get_category_of_resource(cls, mimetype: str) -> str:
        mimetypes = [type for type in cls.model_fields.keys()]

        for type in mimetypes:
            if type in mimetype:
                return type

        return "other"


class Requests(BaseModel):
    aggregation: MimetypeAggregation = MimetypeAggregation()
    items: list[RequestItem] = []
    total_count: int = 0
    total_size: float = 0
