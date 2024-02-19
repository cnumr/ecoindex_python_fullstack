import os
from urllib.parse import urlparse
from ecoindex.cli.helper import replace_localhost_with_hostdocker
from ecoindex.models.cli import CliHost


def test_replace_localhost_with_hostdocker():
    assert replace_localhost_with_hostdocker(
        urlparse("https://test.com/page/").netloc
    ) == CliHost(domain="test.com", netloc="test.com")

    assert replace_localhost_with_hostdocker(
        urlparse("https://localhost:8000/page/").netloc
    ) == CliHost(domain="localhost", netloc="localhost:8000")

    os.environ["DOCKER_CONTAINER"] = "true"
    assert replace_localhost_with_hostdocker(
        urlparse("https://localhost:8000/page/").netloc
    ) == CliHost(domain="host.docker.internal", netloc="host.docker.internal:8000")