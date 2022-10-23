import functools
import hashlib
import typing

from puffin import timer


def hashing_algorithm(
    algorithm: typing.Literal["sha1", "md5"]
) -> typing.Callable[[bytes], str]:
    assert algorithm in hashlib.algorithms_available

    sum_algorithm = getattr(hashlib, algorithm)

    @timer.timer
    @functools.wraps(sum_algorithm)
    def hash_bytes(bs):
        return sum_algorithm(bs).hexdigest()

    return hash_bytes
