import pathlib


def traverse_dir(directory: pathlib.Path):
    for file_path in directory.glob("**/*"):
        if file_path.is_file():
            yield file_path


def load_bytes(path: pathlib.Path):
    with path.open("rb") as f:
        return f.read()
