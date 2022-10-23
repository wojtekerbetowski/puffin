import sys
import pathlib

from . import Storage


class StdinStorage(Storage):
    def store(self, value: dict[pathlib.Path, str]):
        for file_path, hash_value in value.items():
            print(f"{file_path}:{hash_value}")

    def load(self) -> dict[pathlib.Path, str]:
        lines = sys.stdin.readlines()

        return dict(line.strip().split(":") for line in lines)
