from __future__ import annotations

from enum import IntEnum
from typing import Any, SupportsInt, Type, cast


class USCode:
    NEWYORK = 17
    LA = 18


class AreaCode:
    US: Merged[USCode, SupportsInt] = USCode()
    UK: Type[Merged[USCode, SupportsInt]] = UKCode


print(AreaCode.US)  # '5'
print(AreaCode.US.NEWYORK)  # '17'
print(int(AreaCode.US))  # 5
print(AreaCode.UK)
print(AreaCode.UK.LONDON)
print(int(AreaCode.UK))
