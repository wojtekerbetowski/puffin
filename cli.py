import pathlib

import click

from puffin import hashing, files
from puffin.storage import get_storage


@click.group()
def main():
    pass


@main.command()
@click.argument("dir", type=click.Path(exists=True))
@click.option("--algorithm", default="sha1", type=click.Choice(["md5", "sha1"]))
@click.option("--storage", type=click.Path(), required=False)
def verify(dir, algorithm, storage):
    storage = get_storage(storage)

    sums = hash_files(algorithm, dir)

    expected_sums = storage.load()

    assert expected_sums == sums


@main.command()
@click.argument("dir", type=click.Path(exists=True))
@click.option("--storage", type=click.Path(), required=False)
@click.option("--algorithm", default="sha1", type=click.Choice(["md5", "sha1"]))
def calculate(dir, algorithm, storage):
    storage = get_storage(storage)

    sums = hash_files(algorithm, dir)

    storage.store(sums)


def hash_files(algorithm, dir):
    files_to_hash = files.traverse_dir(pathlib.Path(dir))
    hashing_algorithm = hashing.hashing_algorithm(algorithm)
    sums = {
        str(file_path.relative_to(dir)): hashing_algorithm(files.load_bytes(file_path))
        for file_path in files_to_hash
    }
    return sums


if __name__ == "__main__":
    main()
