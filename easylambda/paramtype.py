from typing import Any

from easylambda.aws import Event


class ParamType:
    @staticmethod
    def get(event: Event, name: str) -> Any:
        raise NotImplementedError

    @staticmethod
    def getlist(event: Event, name: str) -> list[Any] | None:
        raise NotImplementedError


class Cookie(ParamType): ...


class Form(ParamType): ...


class File(ParamType): ...
