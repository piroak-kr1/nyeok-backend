from typing import Any, Generic, Type, TypeVar
import pydantic
from pydantic import BaseModel
from pydantic_core import from_json
import requests
import urllib.parse
from env import env
from tourapi.types import Body, ResponseRoot


class BaseParams(BaseModel):
    numOfRows: int
    pageNo: int


class BaseItem(BaseModel):
    pass


P = TypeVar("P", bound=BaseParams)
I = TypeVar("I", bound=BaseItem)


class BaseAPI(Generic[P, I]):
    base_url: str

    def __init__(self, base_url: str, paramT: Type[P], itemT: Type[I]):
        self.base_url = base_url
        self.paramT = paramT
        self.itemT = itemT

    def get(self, params: P) -> ResponseRoot[I]:
        if self.base_url.endswith("/"):
            raise ValueError("base_url should not end with '/'")

        # Get rid of Optional fields if they are None
        param_dict: dict[str, Any] = params.model_dump(exclude_none=True)
        param_dict["serviceKey"] = env.DATAKR_API_KEY
        param_dict["MobileOS"] = "AND"
        param_dict["MobileApp"] = "Nyeok"
        param_dict["_type"] = "json"

        # Encode manually: naive `requests.get` converts % to %25
        param_string = urllib.parse.urlencode(param_dict, safe="%")
        response: requests.Response = requests.get(self.base_url, params=param_string)

        if not response.status_code == 200:
            raise requests.RequestException("Failed to get tourapi", response=response)

        try:
            return ResponseRoot[self.itemT].model_validate(from_json(response.text))
        except pydantic.ValidationError as e:
            raise e from e
        except ValueError as e:
            # TODO: xml parse for error code
            raise ValueError(
                "Failed to deserialize response.text", response.text
            ) from e

    def get_body(self, params: P) -> Body[I]:
        root = self.get(params)
        if root.response.header.resultCode != "0000":
            raise Exception(
                f"API resultCode: {root.response.header.resultCode}\nAPI resultMsg: {root.response.header.resultMsg}"
            )
        return root.response.body

    def get_items(self, params: P) -> list[I]:
        return self.get_body(params).items.item

    def get_items_all(self, params: P) -> list[I]:
        # TODO: client doesn't have to set numOfRows, pageNo
        items: list[I] = []
        params.numOfRows = 10000  # Don't know maximum
        params.pageNo = 1
        while True:
            body = self.get_body(params)
            items.extend(body.items.item)
            if len(items) >= body.totalCount:
                break
            params.pageNo += 1
        return items
