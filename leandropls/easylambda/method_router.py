from __future__ import annotations

from typing import Any, Callable, Literal, TypeVar

from leandropls.easylambda import easylambda

T = TypeVar("T", bound=Callable[..., Any])


class MethodRouter:
    __slots__ = ("methods", "route", "args", "kwargs")

    def __init__(self, route: str, *args, **kwargs) -> None:
        self.methods = {}
        self.route = route
        self.args = args
        self.kwargs = kwargs

    def register(
        self,
        method_name: Literal[
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
            "OPTIONS",
        ],
    ) -> Callable[[T], T]:
        def decorator(func: T) -> T:
            self.methods[method_name] = easylambda(
                self.route,
                methods={method_name},
                *self.args,
                **self.kwargs,
            )(func)
            return func

        return decorator

    @property
    def get(self):
        return self.register("GET")

    @property
    def post(self):
        return self.register("POST")

    @property
    def put(self):
        return self.register("PUT")

    @property
    def delete(self):
        return self.register("DELETE")

    @property
    def patch(self):
        return self.register("PATCH")

    @property
    def options(self):
        return self.register("OPTIONS")

    def __call__(self, event: dict[str, Any], context: Any) -> dict[str, Any]:
        method = event["requestContext"]["http"]["method"]

        try:
            handler = self.methods[method]
        except KeyError:
            return {
                "statusCode": 405,
                "body": "Method Not Allowed",
            }

        return handler(event, context)
