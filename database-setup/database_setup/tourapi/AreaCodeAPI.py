from __future__ import annotations

from typing import Optional
from tourapi.BaseAPI import BaseAPI, BaseItem, BaseParams


class Params(BaseParams):
    areaCode: Optional[int]


class Item(BaseItem):
    rnum: int
    code: str
    name: str


AreaCodeAPI = BaseAPI(
    base_url="http://apis.data.go.kr/B551011/KorService1/areaCode1",
    paramT=Params,
    itemT=Item,
)
