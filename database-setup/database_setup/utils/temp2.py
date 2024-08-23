from typing import SupportsInt, TypeVar


class MetaclassWithInt(type, SupportsInt):
    def __int__(cls) -> int:
        return cls.int_value  # type: ignore

    def __str__(cls):
        return str(int(cls))


T = TypeVar("T")


def class_with_int(cls: type[T], int_value: int) -> type[T]:
    int_value_p = int_value

    class WrappedClass(cls):
        int_value = int_value_p

    return WrappedClass  # type: ignore


class USCode(metaclass=MetaclassWithInt):
    LA = 12
    NEWYORK = 17


class AreaCode:
    US: type[USCode] = class_with_int(USCode, 5)


print(AreaCode.US)  # '5'
print(AreaCode.US.NEWYORK)  # '17'
int(AreaCode.US)  # 5
