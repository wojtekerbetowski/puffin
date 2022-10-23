import hashlib
import json
import pathlib
import sys

import click


@click.group()
def main():
    pass


@main.command()
@click.argument("dir", type=click.Path(exists=True))
@click.option("--algorithm", default="sha1", type=click.Choice(["md5", "sha1"]))
@click.option("--storage", type=click.Path(), required=False)
def verify(dir, algorithm, storage):
    assert algorithm in hashlib.algorithms_available

    sum_algorithm = getattr(hashlib, algorithm)

    def hash_file(file_path):
        with file_path.open("rb") as opened_file:
            file_content = opened_file.read()

        return sum_algorithm(file_content).hexdigest()

    sums = {
        str(file_path.relative_to(dir)): hash_file(file_path)
        for file_path in pathlib.Path(dir).glob('**/*')
        if file_path.is_file()
    }

    if storage:
        with open(storage) as storage_f:
            expected_sums = json.load(storage_f)
    else:
        lines = sys.stdin.readlines()
        expected_sums = dict(
            line.strip().split(":") for line in lines
        )

    assert expected_sums == sums


@main.command()
@click.argument("dir", type=click.Path(exists=True))
@click.option("--storage", type=click.Path(), required=False)
@click.option("--algorithm", default="sha1", type=click.Choice(["md5", "sha1"]))
def calculate(dir, algorithm, storage):
    assert algorithm in hashlib.algorithms_available

    sum_algorithm = getattr(hashlib, algorithm)

    def hash_file(file_path):
        with file_path.open("rb") as opened_file:
            file_content = opened_file.read()

        return sum_algorithm(file_content).hexdigest()

    sums = {
        str(file_path): hash_file(file_path)
        for file_path in pathlib.Path(dir).glob('**/*')
        if file_path.is_file()
    }

    if not storage:
        for file_path, hash_value in sums.items():
            print(f"{file_path}:{hash_value}")
    else:
        with open(storage, "w") as storage_f:
            json.dump(sums, storage_f)


if __name__ == "__main__":
    main()
