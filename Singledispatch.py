from functools import singledispatch


@singledispatch
def func(x):
    print("hi! ")


@func.register
def _(x: int):
    print(x, " I'm int")


@func.register
def _(x: str):
    print(x, " I'm string")


func(1)
func("krkrkr")