from typing import Match

from leandropls.easylambda.aws import Event
from leandropls.easylambda.dependency import Dependency


class Header(Dependency):
    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, event: Event, route: Match) -> str | list[str]:
        try:
            return event.headers[self.name.lower()]
        except KeyError:
            raise KeyError(self.name) from None
