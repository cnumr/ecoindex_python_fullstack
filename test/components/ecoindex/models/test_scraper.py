import pytest
from ecoindex.models.scraper import MimetypeAggregation


@pytest.mark.asyncio
async def test_get_category_of_resource_video() -> None:
    mime_type = "video/mp4"
    assert await MimetypeAggregation.get_category_of_resource(mime_type) == "video"


@pytest.mark.asyncio
async def test_get_category_of_resource_image() -> None:
    mime_type = "image/png"
    assert await MimetypeAggregation.get_category_of_resource(mime_type) == "image"


@pytest.mark.asyncio
async def test_get_category_of_resource_font() -> None:
    mime_type = "font/woff2"
    assert await MimetypeAggregation.get_category_of_resource(mime_type) == "font"


@pytest.mark.asyncio
async def test_get_category_of_resource_css() -> None:
    mime_type = "text/css"
    assert await MimetypeAggregation.get_category_of_resource(mime_type) == "css"


@pytest.mark.asyncio
async def test_get_category_of_resource_javascript() -> None:
    mime_type = "application/javascript"
    assert await MimetypeAggregation.get_category_of_resource(mime_type) == "javascript"


@pytest.mark.asyncio
async def test_get_category_of_resource_other() -> None:
    mime_type = "application/pdf"
    assert await MimetypeAggregation.get_category_of_resource(mime_type) == "other"


if __name__ == "__main__":
    pytest.main()
