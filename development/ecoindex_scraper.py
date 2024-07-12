import asyncio
from pprint import pprint
from uuid import uuid1

from ecoindex.models.compute import ScreenShot
from ecoindex.scraper import EcoindexScraper

scraper = EcoindexScraper(
    url="https://www.kiabi.com",
    screenshot=ScreenShot(id=str(uuid1()), folder="./screenshots"),
)

result = asyncio.run(scraper.get_page_analysis())
all_requests = asyncio.run(scraper.get_all_requests())
requests_by_category = asyncio.run(scraper.get_requests_by_category())

pprint(result)
