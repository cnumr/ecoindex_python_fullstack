class EcoindexScraperException(Exception):
    pass


class EcoindexScraperStatusException(EcoindexScraperException):
    def __init__(self, url: str, status: int, message: str):
        self.message = message
        self.url = url
        self.status = status

    pass
