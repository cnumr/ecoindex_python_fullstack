from tempfile import NamedTemporaryFile
from scrapy.spiders import SitemapSpider


class EcoindexSitemapSpider(SitemapSpider):
    name = "EcoindexSitemapSpider"
    custom_settings = {"LOG_ENABLED": False}

    def __init__(
        self,
        sitemap_urls: list[str],
        temp_file: NamedTemporaryFile,  # type: ignore
        *a,
        **kw,
    ):
        self.sitemap_urls = sitemap_urls
        self.temp_file = temp_file
        super().__init__(*a, **kw)

    def parse(self, response):
        self.temp_file.write(f"{response.url}\n")

