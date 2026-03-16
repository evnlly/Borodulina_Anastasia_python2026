def trace(f):
    def wrapper(*arg, **kwargs):
        res = f(*arg, **kwargs)
        print(f'{f.__name__} , args: {arg}, kwargs: {kwargs}, res: {res}')
        return res

    wrapper.__name__ = f.__name__
    wrapper.__doc__ = f.__doc__
    wrapper.__module__ = f.__module__

    return wrapper


@trace
def say_hi():
    """I'm stupid!!!""
    print('hi!')


if __name__ == '__main__':
    print(say_hi.__name__)
    print(say_hi.__doc__)
    print(say_hi.__module__)