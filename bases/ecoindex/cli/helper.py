from asyncio import run
from ecoindex.config import Settings

from ecoindex.models import Result, WindowSize, CliHost
from ecoindex.scraper import EcoindexScraper


def run_page_analysis(
    url: str,
    window_size: WindowSize,
    wait_after_scroll: int = 3,
    wait_before_scroll: int = 3,
    logger=None,
) -> tuple[Result, bool]:
    """Run the page analysis and return the result and a boolean indicating if the analysis was successful"""
    scraper = EcoindexScraper(
        url=str(url),
        window_size=window_size,
        wait_after_scroll=wait_after_scroll,
        wait_before_scroll=wait_before_scroll,
        page_load_timeout=20,
    )
    try:
        return (run(scraper.get_page_analysis()), True)
    except Exception as e:
        logger.error(f"{url} -- {e.msg if hasattr(e, 'msg') else e}")

        return (
            Result(
                url=url,
                water=0,
                width=window_size.width,
                height=window_size.height,
                size=0,
                nodes=0,
                requests=0,
            ),
            False,
        )


def replace_localhost_with_hostdocker(netloc: str) -> CliHost:
    if Settings().DOCKER_CONTAINER and "localhost" in netloc:
        domain = "host.docker.internal"
        netloc = netloc.replace("localhost", domain)
    elif "localhost" in netloc :
        domain = "localhost"
    else :
        domain = netloc

    return CliHost(domain=domain, netloc=netloc)
