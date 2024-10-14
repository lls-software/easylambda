from typing import Any

from easylambda.aws import Event
from easylambda.paramtype import ParamType


class Header(ParamType):
    @staticmethod
    def get(event: Event, name: str) -> Any:
        try:
            return event.headers[name.lower()]
        except KeyError:
            raise KeyError(name) from None

    @staticmethod
    def getlist(event: Event, name: str) -> list[Any] | None:
        raise NotImplementedError
