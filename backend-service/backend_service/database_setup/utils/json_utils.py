import json
from typing import Any


# json utils
type Json = dict[str, Any]


def json_pretty_print(json_object: Json) -> None:
    json_formatted_str = json.dumps(json_object, indent=2, ensure_ascii=False)
    print(json_formatted_str)


def json_loads(json_string: str) -> Json:
    return json.loads(json_string)
