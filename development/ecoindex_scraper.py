import asyncio
from pprint import pprint

from ecoindex.scraper import EcoindexScraper

pprint(asyncio.run(EcoindexScraper(url="http://ecoindex.fr").get_page_analysis()))
