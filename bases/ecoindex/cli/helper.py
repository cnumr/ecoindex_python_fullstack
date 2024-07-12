from ecoindex.config import Settings
from ecoindex.models import CliHost


def replace_localhost_with_hostdocker(netloc: str) -> CliHost:
    if Settings().DOCKER_CONTAINER and "localhost" in netloc:
        domain = "host.docker.internal"
        netloc = netloc.replace("localhost", domain)
    elif "localhost" in netloc:
        domain = "localhost"
    else:
        domain = netloc

    return CliHost(domain=domain, netloc=netloc)
