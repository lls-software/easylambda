from typing import Any, Match

from leandropls.easylambda.dependency import Dependency


class Path(Dependency):
    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, event: Any, route: Match) -> Any:
        try:
            return route.group(self.name)
        except IndexError:
            raise KeyError(self.name) from None
