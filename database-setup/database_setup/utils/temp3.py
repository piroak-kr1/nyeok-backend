from typing import NewType


class Parent:
    def hello(self):
        return "Hello"


def inherit(cls: type) -> type:
    return type(cls.__name__, (Parent, cls), {})


# @inherit
class Son:
    def world(self):
        return "World"


Parent().hello()
XX = NewType("XX", Son)
XX().world()
