import subprocess


def test_hashing_script():
    output = subprocess.check_output(
        ["python", "my_script.py", "README.md"],
        cwd="..",
    ).decode()

    assert output == "2e1b81a855105ec08e2062438835da6fe6d58c48"
