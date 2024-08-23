from typing import Literal, Optional
from .BaseAPI import BaseAPI, BaseParams, BaseItem


class Params(BaseParams):
    listYN: Optional[Literal["Y", "N"]]  # 목록 구분 (N=Item 없이 개수만 반환)
    # 정렬 기준 (A=제목순, C=수정일순, D=생성일순) 대표이미지 보장: (O=제목순, Q=수정일순, R=생성일순)
    arrange: Optional[Literal["A", "C", "D", "O", "Q", "R"]]
    contentTypeId: Optional[int]
    areaCode: Optional[int]
    sigunguCode: Optional[int]
    cat1: Optional[str]  # 대분류
    cat2: Optional[str]  # 중분류
    cat3: Optional[str]  # 소분류


class Item(BaseItem):
    areacode: int
    sigungucode: int
    title: str
    firstimage: str  # 원본 대표이미지(약 500 * 333)
    firstimage2: str  # 썸네일 이미지 url(약 150 * 100)
    mapx: float
    mapy: float
    contentid: int
    contenttypeid: int
    addr1: str
    addr2: str
    cat1: str
    cat2: str
    cat3: str
    createdtime: int
    modifiedtime: int
    cpyrhtDivCd: str  # 저작권 유형
    mlevel: Optional[str]
    booktour: Optional[str]
    tel: str
    zipcode: Optional[str]


AreaBasedListAPI = BaseAPI(
    "http://apis.data.go.kr/B551011/KorService1/areaBasedList1", Params, Item
)
