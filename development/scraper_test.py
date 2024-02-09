import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

from ecoindex.scraper import EcoindexScraper


async def get_page_analysis(url: str):
    scraper = EcoindexScraper(url=url)
    return (
        await scraper.get_page_analysis(),
        await scraper.get_all_requests(),
        await scraper.get_requests_by_category(),
    )


def run_page_analysis(url: str, index: int):
    analysis, requests, aggregation = asyncio.run(get_page_analysis(url))

    return index, analysis, requests, aggregation


with ThreadPoolExecutor(max_workers=8) as executor:
    future_to_analysis = {}

    url = "https://www.ecoindex.fr"

    for i in range(1):
        print(f"Starting ecoindex {i} analysis")
        future_to_analysis[
            executor.submit(
                run_page_analysis,
                url,
                i,
            )
        ] = url

    for future in as_completed(future_to_analysis):
        try:
            index, analysis, requests, aggregation = future.result()
            print(f"Ecoindex {index}: {analysis}")
            print(f"Requests: {requests}")
            print(f"Aggregation: {aggregation}")
        except Exception as e:
            print(e)
