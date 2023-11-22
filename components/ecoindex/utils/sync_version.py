from functools import lru_cache


@lru_cache(typed=True)
def read_version_from_file(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read().strip()
