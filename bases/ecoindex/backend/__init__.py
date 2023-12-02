import os
from functools import lru_cache


@lru_cache
def get_api_version() -> str:
    current_directory = os.path.dirname(os.path.realpath(__file__))
    version_filename = os.path.join(current_directory, "VERSION")

    with open(version_filename, "r") as f:
        return (f.read()).strip()
