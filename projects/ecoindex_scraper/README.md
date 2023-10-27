# ECOINDEX SCRAPER PYTHON

![Quality check](https://github.com/cnumr/ecoindex_scrap_python/workflows/Quality%20checks/badge.svg)
[![PyPI version](https://badge.fury.io/py/ecoindex-scraper.svg)](https://badge.fury.io/py/ecoindex-scraper)

This module provides a simple interface to get the [Ecoindex](http://www.ecoindex.fr) of a given webpage using module [ecoindex-python](https://pypi.org/project/ecoindex/)

## Requirements

- Python ^3.10 with [pip](https://pip.pypa.io/en/stable/installation/)

## Install

```shell
pip install ecoindex-scraper
```

## Use

### Get a page analysis

You can run a page analysis by calling the function `get_page_analysis()`:

```python
(function) get_page_analysis: (url: AnyHttpUrl, window_size: WindowSize | None = WindowSize(width=1920, height=1080), wait_before_scroll: int | None = 1, wait_after_scroll: int | None = 1) -> Coroutine[Any, Any, Result]
```

Example:

```python
import asyncio
from pprint import pprint

from ecoindex.scrap import EcoindexScraper

pprint(
    asyncio.run(
        EcoindexScraper(url="http://ecoindex.fr")
        .init_chromedriver()
        .get_page_analysis()
    )
)
```

Result example:

```python
Result(width=1920, height=1080, url=AnyHttpUrl('http://ecoindex.fr', ), size=549.253, nodes=52, requests=12, grade='A', score=90.0, ges=1.2, water=1.8, ecoindex_version='5.0.0', date=datetime.datetime(2022, 9, 12, 10, 54, 46, 773443), page_type=None)
```

> **Default behaviour:** By default, the page analysis simulates:
>
> - Uses the last version of chrome (can be set with parameter `chrome_version_main` to a given version. IE `107`)
> - Window size of **1920x1080** pixels (can be set with parameter `window_size`)
> - Wait for **1 second when page is loaded** (can be set with parameter `wait_before_scroll`)
> - Scroll to the bottom of the page (if it is possible)
> - Wait for **1 second after** having scrolled to the bottom of the page (can be set with parameter `wait_after_scroll`)

### Get a page analysis and generate a screenshot

It is possible to generate a screenshot of the analyzed page by adding a `ScreenShot` property to the `EcoindexScraper` object.
You have to define an id (can be a string, but it is recommended to use a unique id) and a path to the screenshot file (if the folder does not exist, it will be created).

```python
import asyncio
from pprint import pprint
from uuid import uuid1

from ecoindex.models import ScreenShot
from ecoindex.scrap import EcoindexScraper

pprint(
    asyncio.run(
        EcoindexScraper(
            url="http://www.ecoindex.fr/",
            screenshot=ScreenShot(id=str(uuid1()), folder="./screenshots"),
        )
        .init_chromedriver()
        .get_page_analysis()
    )
)
```

## Async analysis

You can also run the analysis asynchronously:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

from ecoindex.scrap import EcoindexScraper

def run_page_analysis(url):
    return asyncio.run(
        EcoindexScraper(url=url)
        .init_chromedriver()
        .get_page_analysis()
    )


with ThreadPoolExecutor(max_workers=8) as executor:
    future_to_analysis = {}

    url = "https://www.ecoindex.fr"

    for i in range(10):
        future_to_analysis[
            executor.submit(
                run_page_analysis,
                url,
            )
        ] = (url)

    for future in as_completed(future_to_analysis):
        try:
            print(future.result())
        except Exception as e:
            print(e)
```
