from easylambda.aws import Event
from easylambda.paramtype import ParamType


class Query(ParamType):
    @staticmethod
    def get(event: Event, name: str) -> str:
        try:
            return event.parse_qs()[name][-1]
        except (KeyError, IndexError):
            raise KeyError(name) from None

    @staticmethod
    def getlist(event: Event, name: str) -> list[str]:
        try:
            return event.parse_qs()[name]
        except KeyError:
            return []
