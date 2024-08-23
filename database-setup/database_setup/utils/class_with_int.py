from typing import TypeVar


class MetaClassWithInt(type):
    int_value: int

    def __int__(cls) -> int:
        return cls.int_value

    def __str__(cls):
        return str(int(cls))


T = TypeVar("T")


def class_with_int(cls: type[T], int_value: int) -> type[T]:
    """Decorator that adds an integer value to a class.

    `int(class_with_int(Class, 42))` will return 42.
    """
    int_value_p = int_value

    class WrappedClass(cls, metaclass=MetaClassWithInt):
        int_value = int_value_p

    return WrappedClass  # type: ignore
