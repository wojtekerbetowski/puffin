import abc
import pathlib


class Storage(abc.ABC):
    @abc.abstractmethod
    def store(self, value: dict[pathlib.Path, str]) -> None:
        pass

    @abc.abstractmethod
    def load(self) -> dict[pathlib.Path, str]:
        pass


def get_storage(storage):
    if storage:
        from .json import JSONStorage

        storage = JSONStorage(pathlib.Path(storage))
    else:
        from .stdin import StdinStorage

        storage = StdinStorage()
    return storage
