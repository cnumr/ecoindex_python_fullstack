"""
Ecoindex models
"""

from ecoindex.models.api import (
    ApiEcoindex,
    ApiHealth,
    Host,
    PageApiEcoindexes,
    PageHosts,
)
from ecoindex.models.compute import (
    Ecoindex,
    PageMetrics,
    PageType,
    Request,
    Result,
    ScreenShot,
    WebPage,
    WindowSize,
)
from ecoindex.models.enums import Version
from ecoindex.models.response_examples import (
    example_daily_limit_response,
    example_ecoindex_not_found,
    example_file_not_found,
    example_page_listing_empty,
)
from ecoindex.models.sort import Sort

__all__ = [
    "ApiEcoindex",
    "ApiHealth",
    "Host",
    "PageApiEcoindexes",
    "PageHosts",
    "Ecoindex",
    "PageMetrics",
    "PageType",
    "Request",
    "Result",
    "ScreenShot",
    "WebPage",
    "WindowSize",
    "Version",
    "example_daily_limit_response",
    "example_ecoindex_not_found",
    "example_file_not_found",
    "example_page_listing_empty",
    "Sort",
]
