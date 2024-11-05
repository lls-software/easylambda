from typing import Match

from leandropls.easylambda.aws import Event
from leandropls.easylambda.dependency import Dependency


class Query(Dependency):
    def __init__(self, name: str, is_list: bool = False) -> None:
        self.name = name
        self.is_list = is_list

    def __call__(self, event: Event, route: Match) -> str | list[str]:
        try:
            parsed_qs = event.parse_qs()[self.name]
        except KeyError:
            if self.is_list:
                return []
            raise KeyError(self.name) from None

        if self.is_list:
            return parsed_qs

        try:
            return parsed_qs[-1]
        except IndexError:
            raise KeyError(self.name) from None
