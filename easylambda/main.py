import json
import re

# noinspection PyUnresolvedReferences,PyProtectedMember
from inspect import _empty, signature
from typing import Any, Callable, Literal, Match, Pattern, get_args, get_origin

from pydantic import ValidationError, validate_call

from easylambda.aws import Event, Response
from easylambda.errors import (
    HttpError,
    HttpMethodNotAllowed,
    HttpNotFound,
    HttpUnprocessableEntity,
)
from easylambda.paramtype import ParamType
from easylambda.path import Path

ALL_METHODS = frozenset(("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"))


def get_handler_arguments(handler) -> dict[str, tuple[bool, bool, ParamType | None]]:
    """Get the arguments from the handler signature.

    :param handler: The handler to get the arguments from.
    :returns: The arguments from the handler signature.
    """
    arguments = {}
    for k, p in signature(handler).parameters.items():
        has_default = p.default is not _empty
        v = p.annotation
        if v is _empty:
            # No type hint
            is_list = False
            param_type = None
        elif not hasattr(v, "__metadata__"):
            # Unannotated
            is_list = get_origin(v) is list
            param_type = None
        else:
            # Annotated
            is_list = get_origin(get_args(v)[0]) is list
            try:
                param_type = next(m for m in v.__metadata__ if isinstance(m, ParamType))
            except StopIteration:
                param_type = None
        arguments[k] = (has_default, is_list, param_type)
    return arguments


def fill_handler_kwargs(
    event: Event,
    url_match: Match[str],
    handler_arguments: dict[str, tuple[bool, bool, ParamType | Path | None]],
) -> dict[str, Any]:
    """Fill the handler arguments from the event.

    :param event: The event to extract the arguments from.
    :param url_match: The URL match object.
    :param handler_arguments: The handler arguments from its signature.
    :returns: The filled kwargs.
    """
    kwargs = {}
    for k, (has_default, is_list, param_type) in handler_arguments.items():
        if k in kwargs:
            continue
        try:
            if param_type is None:
                kwargs[k] = Path.get(url_match, k)
            elif isinstance(param_type, Path):
                kwargs[k] = param_type.get(url_match, k)
            elif is_list:
                kwargs[k] = param_type.getlist(event, k)
            else:
                kwargs[k] = param_type.get(event, k)
        except KeyError:
            if has_default:
                continue
            raise
    return kwargs


class Application:
    """A wrapper to simplify the creation of AWS Lambda handlers."""

    __slots__ = ("methods", "url_regex", "handler", "handler_arguments")

    def __init__(
        self,
        methods: set[str],
        url_regex: Pattern[str],
        handler: callable,
        handler_arguments: dict[str, tuple[bool, bool, ParamType | None]],
    ) -> None:
        self.methods = methods
        self.url_regex = url_regex
        self.handler = handler
        self.handler_arguments = handler_arguments

    @validate_call
    def __call__(
        self,
        event: dict[str, Any],
        context: Any,
    ) -> dict[str, Any]:
        """The AWS Lambda handler."""
        # noinspection PyBroadException
        try:
            return self.generate_response(Event.model_validate(event)).model_dump()
        except HttpError as e:
            return e.to_response().model_dump()

    def generate_response(self, event: Event) -> Response:
        """Generate the response for the event."""
        http = event.requestContext.http
        url_match = self.url_regex.match(http.path)
        if url_match is None:
            raise HttpNotFound()

        if http.method not in self.methods:
            raise HttpMethodNotAllowed()

        # Fill the handler arguments
        try:
            kwargs = fill_handler_kwargs(
                event=event,
                url_match=url_match,
                handler_arguments=self.handler_arguments,
            )
        except KeyError as e:
            raise HttpUnprocessableEntity(str(e))

        # Call the handler
        try:
            handler_response = self.handler(**kwargs)
        except ValidationError as e:
            raise HttpUnprocessableEntity(str(e))

        # Return the response
        return Response(
            statusCode=200,
            headers={"Content-Type": "application/json"},
            body=json.dumps(handler_response),
        )


# noinspection PyDefaultArgument
def easylambda(
    route: str,
    *,
    methods: set[
        Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    ] = ALL_METHODS,
) -> Callable[[callable], Callable[[dict[str, Any], Any], dict[str, Any]]]:
    """Turns a EasyLambda Function into an AWS Lambda handler.

    :params route: The URL route to match.
    :params methods: The HTTP methods to match.
    :returns: A decorator that turns a function into a Lambda handler.
    """

    def decorator(handler: callable):
        # Introspect the handler to determine the arguments
        handler_arguments = get_handler_arguments(handler)

        # Create the URL map and wrap the handler
        url_regex = re.compile(
            r"^" + re.sub(r"{([^}]+)}", r"(?P<\1>[^/]+)", route) + r"$"
        )

        # Wrap the handler for validation
        handler = validate_call(validate_return=True)(handler)

        return Application(
            methods=methods,
            url_regex=url_regex,
            handler=handler,
            handler_arguments=handler_arguments,
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
