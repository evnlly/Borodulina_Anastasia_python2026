from warnings import warn
from functools import wraps


def deprecated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        warn("don't use me I'm outdated!", category=UserWarning)
        return func(*args, **kwargs)
    return wrapper


@deprecated
def f(n) :
    return n


if __name__ == '__main__':
    print(f(10))