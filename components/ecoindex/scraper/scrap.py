import json
import os
from datetime import datetime
from time import sleep

from ecoindex.compute.ecoindex import compute_ecoindex
from ecoindex.models.compute import PageMetrics, Result, ScreenShot, WindowSize
from ecoindex.utils.screenshots import convert_screenshot_to_webp, set_screenshot_rights
from playwright.async_api import async_playwright
from slugify import slugify
from typing_extensions import deprecated


class EcoindexScraperException(Exception):
    pass


class EcoindexScraper:
    def __init__(
        self,
        url: str,
        window_size: WindowSize = WindowSize(width=1920, height=1080),
        wait_before_scroll: float = 1,
        wait_after_scroll: float = 1,
        screenshot: ScreenShot | None = None,
        screenshot_uid: int | None = None,
        screenshot_gid: int | None = None,
        page_load_timeout: int = 20,
    ):
        self.url = url
        self.window_size = window_size
        self.wait_before_scroll = wait_before_scroll
        self.wait_after_scroll = wait_after_scroll
        self.screenshot = screenshot
        self.screenshot_uid = screenshot_uid
        self.screenshot_gid = screenshot_gid
        self.page_load_timeout = page_load_timeout
        self.all_requests = {"entries": [], "total_count": 0, "total_size": 0}

        self.now = datetime.now()
        date = self.now.strftime("%Y-%m-%d-%H-%M-%S")
        slug = slugify(self.url)

        self.slugified_session_name = f"ecoindex-{slug}-{date}"
        self.har_temp_file_path = f"/tmp/{self.slugified_session_name}.har"

    @deprecated("This method is useless with new version of EcoindexScraper")
    def init_chromedriver(self):
        return self

    async def get_page_analysis(self) -> Result:
        page_metrics = await self.scrap_page()
        ecoindex = await compute_ecoindex(**page_metrics.model_dump())

        return Result(
            **ecoindex.model_dump(),
            **self.window_size.model_dump(),
            **page_metrics.model_dump(),
            date=self.now,
            url=self.url,
        )

    async def scrap_page(self) -> PageMetrics:
        async with async_playwright() as p:
            browser = await p.firefox.launch()
            self.page = await browser.new_page(
                record_har_path=self.har_temp_file_path,
                screen=self.window_size.model_dump(),
            )
            response = await self.page.goto(self.url)
            if response.status != 200:
                raise EcoindexScraperException(
                    f"Error {response.status} for {self.url}"
                )

            await self.page.wait_for_load_state()
            sleep(self.wait_before_scroll)
            await self.generate_screenshot()
            await self.page.evaluate(
                "window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })"
            )
            sleep(self.wait_after_scroll)
            total_nodes = await self.get_nodes_count()

            await self.page.close()
            await browser.close()

        await self.get_requests_from_har_file()

        return PageMetrics(
            size=self.all_requests["total_size"] / 1000,
            nodes=total_nodes,
            requests=self.all_requests["total_count"],
        )

    async def generate_screenshot(self) -> None:
        if self.screenshot and self.screenshot.folder and self.screenshot.id:
            await self.page.screenshot(path=self.screenshot.get_png())
            convert_screenshot_to_webp(self.screenshot)
            set_screenshot_rights(
                screenshot=self.screenshot,
                uid=self.screenshot_uid,
                gid=self.screenshot_gid,
            )

    async def get_requests_from_har_file(self):
        with open(self.har_temp_file_path, "r") as f:
            trace = json.load(f)

            for entry in trace["log"]["entries"]:
                self.all_requests["entries"].append(
                    {
                        "url": entry["request"]["url"],
                        "mime_type": entry["response"]["content"]["mimeType"],
                        "status": entry["response"]["status"],
                        "size": entry["response"]["_transferSize"],
                    }
                )

                self.all_requests["total_count"] += 1
                self.all_requests["total_size"] += entry["response"]["_transferSize"]

        os.remove(self.har_temp_file_path)

    async def get_nodes_count(self):
        nodes = await self.page.locator("*").count()
        svgs = await self.page.locator("//*[local-name()='svg']//*").count()

        return nodes - svgs
