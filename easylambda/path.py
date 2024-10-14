from re import Match
from typing import Any


class Path:
    @staticmethod
    def get(match: Match, name: str) -> Any:
        try:
            return match.group(name)
        except IndexError:
            raise KeyError(name) from None
