import hashlib
import typing


def hashing_algorithm(
    algorithm: typing.Literal["sha1", "md5"]
) -> typing.Callable[[bytes], str]:
    assert algorithm in hashlib.algorithms_available

    sum_algorithm = getattr(hashlib, algorithm)

    def hash_bytes(bs):
        return sum_algorithm(bs).hexdigest()

    return hash_bytes
