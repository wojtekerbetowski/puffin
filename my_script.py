import os
import sys
from hashlib import sha1


def main():
    filename = sys.argv[1]

    with open(filename, "rb") as f:
        file_content = f.read()

    hashsum = sha1(file_content).hexdigest()

    print(hashsum, end="")


if __name__ == "__main__":
    main()
