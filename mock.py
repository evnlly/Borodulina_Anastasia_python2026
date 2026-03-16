from functools import wraps


def mock(return_value):
    def param(function):
        @wraps(function)
        def wrapper(*args, **kwarg):
            return return_value
        return wrapper
    return param


@mock(return_value='\<\(_o_)\>')
def f1(x, y, z):
    return x + y + z


@mock(return_value='не судьба тебе вызваться')
def f2(z=1, y=2):
    return z * y


print(f1(1, 2, 3))
print(f2(9, y=1))