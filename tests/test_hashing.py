import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

import my_script
from my_script import main


@pytest.fixture
def hello_file(tmpdir):
    test_file = Path(tmpdir, "filename")

    with(test_file.open("w")) as f:
        f.write("Hello")

    yield test_file.absolute()


@pytest.fixture
def runner():
    return CliRunner()


class TestHashVerification:

    def test_fails_on_missing_file(self, runner):
        p = runner.invoke(my_script.verify, ["missing_file"])

        assert p.exit_code

    def test_successful_verification(self, hello_file: Path, runner):
        expected_sum = "f7ff9e8b7bb2e09b70935a5d785e0cc5d9d0abf0"

        command = runner.invoke(
            my_script.main,
            [
                "verify",
                str(hello_file),
                expected_sum,
            ],
        )

        assert command.exit_code == 0

    def test_verification_failure(self, hello_file: Path, runner):
        expected_sum = "wrong sum"

        command = runner.invoke(
            my_script.main,
            [
                "verify",
                str(hello_file),
                expected_sum,
            ],
        )

        assert command.exit_code != 0

    def test_verification_wrong_algo(self, hello_file: Path, runner):
        expected_sum = "f7ff9e8b7bb2e09b70935a5d785e0cc5d9d0abf0"

        command = runner.invoke(
            my_script.main,
            [
                "verify",
                str(hello_file),
                expected_sum,
                "--algorithm",
                "md5",
            ],
        )

        assert command.exit_code != 0
