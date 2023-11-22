import os

import tomli

current_directory = os.path.dirname(os.path.realpath(__file__))
pyproject_file = os.path.join(
    current_directory, "..", "..", "..", "projects", "ecoindex_api", "pyproject.toml"
)
version_file = os.path.join(current_directory, "..", "compute", "VERSION")


def main() -> None:
    with open(pyproject_file, "rb") as pyproject_fp, open(
        version_file, "w"
    ) as version_fp:
        data = tomli.load(pyproject_fp)
        ecoindex_compute_version = data["tool"]["poetry"]["version"]
        version_fp.write(ecoindex_compute_version)

    print(f"ecoindex_compute_version = {ecoindex_compute_version!r}")


if __name__ == "__main__":
    main()
