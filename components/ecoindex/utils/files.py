from abc import ABC, abstractmethod
from csv import DictWriter
from json import dump
from os import makedirs
from os.path import dirname, exists

from ecoindex.models import ExportFormat, Language, Result
from yaml import safe_load as load_yaml


def create_folder(path: str) -> None:
    if not exists(path):
        makedirs(path)


class File(ABC):
    def __init__(
        self,
        filename: str,
        results: list[Result],
        export_format: ExportFormat | None = ExportFormat.csv,
    ):
        self.filename = filename
        self.results = results
        self.export_format = export_format

    @abstractmethod
    def write(self) -> None:
        pass


class CsvFile(File):
    def write(self) -> None:
        headers = self.results[0].__dict__

        with open(self.filename, "w") as fp:
            writer = DictWriter(fp, fieldnames=headers)

            writer.writeheader()
            for ecoindex in self.results:
                writer.writerow(ecoindex.__dict__)


class JsonFile(File):
    def write(self) -> None:
        with open(self.filename, "w") as fp:
            dump(
                obj=[ecoindex.__dict__ for ecoindex in self.results],
                fp=fp,
                indent=4,
                default=str,
            )


def write_results_to_file(
    filename: str,
    results: list[Result],
    export_format: ExportFormat | None = ExportFormat.csv,
) -> None:
    if export_format == ExportFormat.csv:
        CsvFile(filename=filename, results=results, export_format=export_format).write()

    if export_format == ExportFormat.json:
        JsonFile(
            filename=filename, results=results, export_format=export_format
        ).write()


def write_urls_to_file(file_prefix: str, urls: list[str]) -> None:
    tmp_input_folder = "/tmp/ecoindex-cli/input"
    create_folder(tmp_input_folder)
    with open(
        file=f"{tmp_input_folder}/{file_prefix}.csv", mode="w"
    ) as input_urls_file:
        for url in urls:
            input_urls_file.write(f"{str(url).strip()}\n")


def get_translations(language: Language) -> dict:
    filename = f"{dirname(__file__)}/cli_translations/{language.value}.yml"
    with open(filename) as fp:
        return load_yaml(fp)
