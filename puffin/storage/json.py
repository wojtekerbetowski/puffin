import json
import pathlib

from . import Storage


class JSONStorage(Storage):
    def __init__(self, path: pathlib.Path):
        self.path = path

    def store(self, value: dict[pathlib.Path, str]):
        with self.path.open("w") as f:
            json.dump(value, f)

    def load(self) -> dict[pathlib.Path, str]:
        with self.path.open() as f:
            return json.load(f)
