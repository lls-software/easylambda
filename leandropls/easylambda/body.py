import json
from typing import Any, Match

from leandropls.easylambda.aws import Event
from leandropls.easylambda.dependency import Dependency

_Undefined = object()


class Body(Dependency):
    _cache = _Undefined
    _cache_request_id = _Undefined

    def __call__(self, event: Event, route: Match) -> Any:
        request_id = event.requestContext.requestId
        if self._cache_request_id != request_id:
            match event.content_type:
                case "application/json":
                    self._cache_request_id = request_id
                    try:
                        self._cache = json.loads(event.body)
                    except json.JSONDecodeError:
                        self._cache = None
                case _:
                    self._cache_request_id = request_id
                    self._cache = event.body
        return self._cache
