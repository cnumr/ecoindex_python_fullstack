from enum import Enum


class Version(str, Enum):
    v0 = "v0"
    v1 = "v1"

    def get_version_number(self) -> int:
        return int(self.value[1:])
