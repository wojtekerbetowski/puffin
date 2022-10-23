import json
from pathlib import Path

import pytest
from click.testing import CliRunner

import my_script


def hello_file(tmpdir):
    test_file = Path(tmpdir, "a")

    with(test_file.open("w")) as f:
        f.write("Hello")

    yield test_file.absolute()


@pytest.fixture
def runner():
    return CliRunner()


class TestHashVerification:

    def test_empty_directory_stdout(self, runner, tmpdir):
        command = runner.invoke(
            my_script.calculate,
            [
                str(tmpdir),
            ],
        )

        assert command.exit_code == 0

        assert command.stdout == ""

    def test_empty_directory_json(self, runner, tmpdir):
        storage = Path(tmpdir, "storage.json")

        command = runner.invoke(
            my_script.calculate,
            [
                str(tmpdir),
                "--storage",
                str(storage),
            ],
        )

        assert command.exit_code == 0

        assert command.stdout == ""

        with storage.open() as f:
            out = json.load(f)

        assert out == {}

    def test_successful_verification_stdin(self, tmpdir, runner):
        file_path = "filename"
        file_content = "Hello"
        expected_sum = "f7ff9e8b7bb2e09b70935a5d785e0cc5d9d0abf0"

        with Path(tmpdir, file_path).open("w") as f:
            f.write(file_content)


        command = runner.invoke(
            my_script.main,
            [
                "verify",
                str(tmpdir),
            ],
            input=f"{file_path}:{expected_sum}",
        )

        assert command.exit_code == 0

    def test_successful_verification_json(self, tmpdir, runner):
        hash_dir = Path(tmpdir, "dir")
        hash_dir.mkdir()

        file_path = "filename"
        file_content = "Hello"
        expected_sum = "f7ff9e8b7bb2e09b70935a5d785e0cc5d9d0abf0"

        with Path(hash_dir, file_path).open("w") as f:
            f.write(file_content)

        with Path(tmpdir, "storage.json").open("w") as f:
            json.dump({
                file_path: expected_sum,
            }, f)

        command = runner.invoke(
            my_script.main,
            [
                "verify",
                str(Path(tmpdir, "dir")),
                "--storage",
                str(Path(tmpdir, "storage.json")),
            ],
        )

        assert command.exit_code == 0

    def test_failed_verification_stdin(self, tmpdir, runner):
        file_path = "filename"
        file_content = "Hello"
        expected_sum = "wrong hash"

        with Path(tmpdir, file_path).open("w") as f:
            f.write(file_content)


        command = runner.invoke(
            my_script.main,
            [
                "verify",
                str(tmpdir),
            ],
            input=f"{file_path}:{expected_sum}",
        )

        assert command.exit_code != 0

    def test_failed_verification_json(self, tmpdir, runner):
        hash_dir = Path(tmpdir, "dir")
        hash_dir.mkdir()

        file_path = "filename"
        file_content = "Hello"
        expected_sum = "wrong hash"

        with Path(hash_dir, file_path).open("w") as f:
            f.write(file_content)

        with Path(tmpdir, "storage.json").open("w") as f:
            json.dump({
                file_path: expected_sum,
            }, f)

        command = runner.invoke(
            my_script.main,
            [
                "verify",
                str(Path(tmpdir, "dir")),
                "--storage",
                str(Path(tmpdir, "storage.json")),
            ],
        )

        assert command.exit_code != 0
