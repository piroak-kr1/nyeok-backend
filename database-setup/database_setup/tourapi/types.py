from __future__ import annotations
from typing import Generic, TypeVar
from pydantic import BaseModel
import math

ItemT = TypeVar("ItemT")


class ResponseRoot(BaseModel, Generic[ItemT]):
    response: Response[ItemT]


class Response(BaseModel, Generic[ItemT]):
    header: Header
    body: Body[ItemT]


class Header(BaseModel):
    resultCode: str
    resultMsg: str


class Body(BaseModel, Generic[ItemT]):
    items: Items[ItemT]
    numOfRows: int  # 한 페이지 결과 수
    pageNo: int  # 페이지 번호
    totalCount: int  # 전체 결과 수

    @property
    def totalPage(self) -> int:
        return math.ceil(self.totalCount / self.numOfRows)


class Items(BaseModel, Generic[ItemT]):
    item: list[ItemT]
