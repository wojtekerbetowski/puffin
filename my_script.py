import os
import sys
import hashlib

import click


@click.group()
def main():
    pass


@main.command()
@click.argument("filename", type=click.Path())
@click.argument("sum", type=str)
@click.option("--algorithm", default="sha1", type=click.Choice(["md5", "sha1"]))
def verify(filename, algorithm, sum):
    with open(filename, "rb") as f:
        file_content = f.read()

    assert algorithm in hashlib.algorithms_available

    sum_algorithm = getattr(hashlib, algorithm)
    hashsum = sum_algorithm(file_content).hexdigest()

    assert hashsum == sum


if __name__ == "__main__":
    main()
