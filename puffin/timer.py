import functools
import time


def timer(function):
    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        start = time.time()

        try:
            return function(*args, **kwargs)
        finally:
            millis = time.time() - start
            with open("timetrack.csv", "a") as f:
                f.write(f"{function.__name__},{millis}\n")

    return wrapped
