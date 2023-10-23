import asyncio
from pprint import pprint

from ecoindex.scraper import EcoindexScraper

pprint(
    asyncio.run(
        EcoindexScraper(
            url="https://www.ecoindex.fr",
        )
        .init_chromedriver()
        .get_page_analysis()
    )
)
