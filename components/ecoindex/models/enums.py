from enum import Enum


class Version(str, Enum):
    v0 = "v0"
    v1 = "v1"

    def get_version_number(self) -> int:
        return int(self.value[1:])


class ExportFormat(Enum):
    csv = "csv"
    json = "json"


class Language(Enum):
    fr = "fr"
    en = "en"


class TaskStatus(str, Enum):
    FAILURE = "FAILURE"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"


class BadgeTheme(str, Enum):
    dark = "dark"
    light = "light"


class Grade(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
