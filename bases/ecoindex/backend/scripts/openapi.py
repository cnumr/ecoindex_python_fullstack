from json import dumps

from ecoindex.backend.main import app


def main() -> None:
    openapi = app.openapi()

    print(dumps(openapi, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
