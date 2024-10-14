import json
from typing import Any

from easylambda.aws import Event
from easylambda.paramtype import ParamType


class Body(ParamType):
    @staticmethod
    def get(event: Event, name: str) -> Any:
        content_type = event.content_type
        if content_type is None:
            return None
        if content_type.startswith("text/"):
            return event.body
        if content_type == "application/json":
            return json.loads(event.body)
        return None

    @staticmethod
    def getlist(event: Event, name: str) -> list[Any] | None:
        if event.content_type == "application/json":
            ans = json.loads(event.body)
            if isinstance(ans, list):
                return ans
        return None
