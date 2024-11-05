import json

from leandropls.easylambda.aws import Response


class HttpError(Exception):
    def __init__(self, status_code: int = 500, message: str | None = None) -> None:
        self.status_code = status_code
        self.message = message

    def to_response(self) -> Response:
        return Response(
            statusCode=self.status_code,
            headers={"Content-Type": "application/json"},
            body=json.dumps({"detail": self.message}),
        )


class HttpBadRequest(HttpError):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=400, message=message)


class HttpUnauthorized(HttpError):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(status_code=401, message=message)


class HttpForbidden(HttpError):
    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(status_code=403, message=message)


class HttpNotFound(HttpError):
    def __init__(self, message: str = "Not Found") -> None:
        super().__init__(status_code=404, message=message)


class HttpMethodNotAllowed(HttpError):
    def __init__(self, message: str = "Method Not Allowed") -> None:
        super().__init__(status_code=405, message=message)


class HttpConflict(HttpError):
    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(status_code=409, message=message)


class HttpUnprocessableEntity(HttpError):
    def __init__(self, message: str = "Unprocessable Entity") -> None:
        super().__init__(status_code=422, message=message)


class HttpInternalServerError(HttpError):
    def __init__(self, message: str = "Internal Server Error") -> None:
        super().__init__(status_code=500, message=message)


class HttpNotImplemented(HttpError):
    def __init__(self, message: str = "Not Implemented") -> None:
        super().__init__(status_code=501, message=message)


class HttpServiceUnavailable(HttpError):
    def __init__(self, message: str = "Service Unavailable") -> None:
        super().__init__(status_code=503, message=message)


class HttpGatewayTimeout(HttpError):
    def __init__(self, message: str = "Gateway Timeout") -> None:
        super().__init__(status_code=504, message=message)
