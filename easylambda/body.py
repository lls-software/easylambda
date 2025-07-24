import json
from base64 import b64decode
from typing import Any, Match

from easylambda.aws import Event
from easylambda.dependency import Dependency

_Undefined = object()


class Body(Dependency):
    _cache = _Undefined
    _cache_request_id = _Undefined

    def __call__(self, event: Event, route: Match) -> Any:
        request_id = event.requestContext.requestId
        if event.isBase64Encoded:
            body = b64decode(event.body).decode()
        else:
            body = event.body
        if self._cache_request_id != request_id:
            match event.content_type:
                case "application/json":
                    self._cache_request_id = request_id
                    try:
                        self._cache = json.loads(body)
                    except json.JSONDecodeError:
                        self._cache = None
                case _:
                    self._cache_request_id = request_id
                    self._cache = body
        return self._cache
