from warnings import warn
from functools import wraps


def deprecated_v2( message):
    def deprecated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warn(message, category=UserWarning)
            return func(*args, **kwargs)
        return wrapper
    return deprecated


@deprecated_v2("bebebe")
def f(n) :
    return n


if __name__ == '__main__':
    print(f(10))