from abc import abstractmethod
from typing import Any, Match

from easylambda.aws import Event


class Dependency:
    __slots__ = ()

    @abstractmethod
    def __call__(self, event: Event, route: Match) -> Any:
        raise NotImplementedError
