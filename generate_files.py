import pathlib
import random
import string

import click


@click.command()
@click.argument("n", type=int)
@click.argument("dir", type=click.Path(exists=False))
def main(n, dir):
    pathlib.Path(dir).mkdir()

    for i in range(n):
        with open(pathlib.Path(dir, f"file_{i}"), "w") as f:
            f.write(random.choice(string.ascii_letters))


if __name__ == "__main__":
    main()
