from pydantic import BaseModel

class CliHost(BaseModel):
    domain: str
    netloc: str

