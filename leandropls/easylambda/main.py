import json
import re

# noinspection PyUnresolvedReferences,PyProtectedMember
from inspect import _empty, signature
from typing import Any, Callable, Literal, Match, Pattern

from pydantic import BaseModel, ValidationError, validate_call

from leandropls.easylambda.aws import Event, Response
from leandropls.easylambda.depends import Depends
from leandropls.easylambda.errors import (
    HttpError,
    HttpInternalServerError,
    HttpMethodNotAllowed,
    HttpNotFound,
    HttpUnprocessableEntity,
)

ALL_METHODS = frozenset(("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"))


class Application:
    """A wrapper to simplify the creation of AWS Lambda handlers."""

    __slots__ = ("methods", "url_regex", "handler", "print_errors")

    def __init__(
        self,
        methods: set[str],
        url_regex: Pattern[str],
        handler: Callable[[Event, Match], Any],
        print_errors: bool,
    ) -> None:
        self.methods = methods
        self.url_regex = url_regex
        self.handler = handler
        self.print_errors = print_errors

    @validate_call
    def __call__(
        self,
        event: dict[str, Any],
        context: Any,
    ) -> dict[str, Any]:
        """The AWS Lambda handler."""
        # noinspection PyBroadException
        try:
            response = self.generate_response(Event.model_validate(event)).model_dump()
        except HttpError as e:
            response = e.to_response().model_dump()
            if self.print_errors:
                print(response, flush=True)
        return response

    def generate_response(self, event: Event) -> Response:
        """Generate the response for the event."""
        # Check the URL match
        http = event.requestContext.http
        url_match = self.url_regex.match(http.path)
        if url_match is None:
            raise HttpNotFound()

        # Check the HTTP method
        if http.method not in self.methods:
            raise HttpMethodNotAllowed()

        # Call the handler
        try:
            handler_response = self.handler(event, url_match)
        except ValidationError as e:
            raise HttpUnprocessableEntity(str(e))

        # Check the handler response
        if isinstance(handler_response, Response):
            return handler_response
        elif isinstance(handler_response, BaseModel):
            status, body = 200, handler_response.model_dump_json()
        elif handler_response is None:
            status, body = 204, ""
        else:
            try:
                status, body = 200, json.dumps(handler_response)
            except TypeError:
                raise HttpInternalServerError(message="Invalid handler response.")

        # Return the response
        return Response(
            statusCode=status,
            headers={"Content-Type": "application/json"},
            body=body,
        )


# noinspection PyDefaultArgument
def easylambda(
    route: str,
    *,
    methods: set[Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]] = ALL_METHODS,
    print_errors: bool = False,
) -> Callable[[callable], Callable[[dict[str, Any], Any], dict[str, Any]]]:
    """Turns a EasyLambda Function into an AWS Lambda handler.

    :params route: The URL route to match.
    :params methods: The HTTP methods to match.
    :returns: A decorator that turns a function into a Lambda handler.
    """

    def decorator(handler: callable):
        # Create the URL map and wrap the handler
        url_regex = re.compile(r"^" + re.sub(r"{([^}]+)}", r"(?P<\1>[^/]+)", route) + r"$")

        # Wrap the handler for dependency injection and validation
        handler = Depends(validate_call(validate_return=True)(handler))

        return Application(
            methods=methods,
            url_regex=url_regex,
            handler=handler,
            print_errors=print_errors,
        )

    return decorator


def get(
    route: str,
) -> Callable[[callable], Callable[[dict[str, Any], Any], dict[str, Any]]]:
    return easylambda(route, methods={"GET"})


def post(
    route: str,
) -> Callable[[callable], Callable[[dict[str, Any], Any], dict[str, Any]]]:
    return easylambda(route, methods={"POST"})


def put(
    route: str,
) -> Callable[[callable], Callable[[dict[str, Any], Any], dict[str, Any]]]:
    return easylambda(route, methods={"PUT"})


def delete(
    route: str,
) -> Callable[[callable], Callable[[dict[str, Any], Any], dict[str, Any]]]:
    return easylambda(route, methods={"DELETE"})


def patch(
    route: str,
) -> Callable[[callable], Callable[[dict[str, Any], Any], dict[str, Any]]]:
    return easylambda(route, methods={"PATCH"})


def options(
    route: str,
) -> Callable[[callable], Callable[[dict[str, Any], Any], dict[str, Any]]]:
    return easylambda(route, methods={"OPTIONS"})
