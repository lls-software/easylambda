from inspect import Signature, isclass, signature
from typing import Annotated, Any, Callable, Match, TypeVar, get_args, get_origin

from leandropls.easylambda.aws import Event
from leandropls.easylambda.dependency import Dependency

T = TypeVar("T")


class Depends(Dependency):
    """Dependency injection class."""

    def __init__(self, func: Callable[..., T]) -> None:
        """Initialize the dependency injection class.

        :param func: The function to inject the dependencies.
        """
        self.func = func
        func_kwargs: dict[str, Callable[[Event, Match], Any]] = {}
        self.func_kwargs = func_kwargs
        for k, p in signature(func).parameters.items():
            v = p.annotation

            if v is Event:
                # expected type is Event
                func_kwargs[k] = lambda event, match: event
                continue

            has_default = p.default is not Signature.empty
            is_annotated = get_origin(v) is Annotated
            if not is_annotated:
                # argument is not annotated
                if not has_default:
                    # argument is not annotated and has no default value
                    raise ValueError(
                        f"Parameter {k} of {func} must be annotated with "
                        f"Depends to use it as a dependency."
                    )

                # argument is not annotated but has a default value
                func_kwargs[k] = lambda event, match: p.default
                continue

            # if is annotated
            for m in get_args(v):
                if isinstance(m, Dependency):
                    # argument is a dependency
                    if has_default:
                        func_kwargs[k] = try_except(m, KeyError, p.default)
                    else:
                        func_kwargs[k] = m
                    break
                elif isclass(m) and issubclass(m, Dependency):
                    # argument is a Dependency, but not instantiated
                    if has_default:
                        func_kwargs[k] = try_except(m(), KeyError, p.default)
                    else:
                        func_kwargs[k] = m()
                    break
            else:
                # argument is annotated but not with Depends
                raise ValueError(
                    f"Parameter {k} of {func} must be annotated with "
                    f"Depends to use it as a dependency."
                )

    def __call__(self, event: Event, match: Match) -> T:
        """Call the function with the dependencies.

        :param event: The event to inject into the dependencies.
        :param match: The route match to inject into the dependencies.
        :returns: The result of the function.
        """
        return self.func(**{k: v(event, match) for k, v in self.func_kwargs.items()})


V = TypeVar("V")


def try_except(
    func: Callable[..., V],
    exception: type[BaseException],
    default: V,
) -> Callable[..., V]:
    """Wrap a function with a try-except block.

    :param func: The function to wrap.
    :param exception: The exception to catch.
    :param default: The default value to return.
    :returns: The wrapped function.
    """

    # noinspection PyBroadException
    def func_wrapper(*args, **kwargs) -> V:
        try:
            return func(*args, **kwargs)
        except exception:
            return default

    return func_wrapper
