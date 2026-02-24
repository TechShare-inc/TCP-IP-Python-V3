"""Decorator for forwarding DobotRobot methods to sub-objects.

Usage::

    from dobot_api_v3._forward import forward_to
    from dobot_api_v3.responses import AckResponse

    class DobotRobot:
        @forward_to("dashboard", AckResponse)
        def disable_robot(self) -> AckResponse:
            \"\"\"Disable the robot arm.\"\"\"

The decorator replaces the method body with a delegation to
``self.<target_attr>.<method_name>(*args, **kwargs)`` whose raw string result
is parsed through :func:`~dobot_api_v3.responses.parse_response`.

The original signature and docstring are preserved via :func:`functools.wraps`
so that IDEs and type-checkers still see the correct interface.
"""

from __future__ import annotations

import functools
from typing import Any, Callable, Type, TypeVar

from .responses import parse_response

_ResponseT = TypeVar("_ResponseT")


def forward_to(
    target_attr: str,
    response_type: Type[_ResponseT],
) -> Callable[[Callable[..., Any]], Callable[..., _ResponseT]]:
    """Decorator factory that delegates a method to a sub-object and parses the result.

    Args:
        target_attr: Name of the instance attribute that holds the delegate
            object (e.g. ``"dashboard"`` or ``"move"``).
        response_type: Response dataclass type to pass to
            :func:`~dobot_api_v3.responses.parse_response`.

    Returns:
        A decorator that replaces the decorated method body with a delegation
        call, while preserving the original signature and docstring.

    Example:
        >>> @forward_to("dashboard", AckResponse)
        ... def disable_robot(self) -> AckResponse:
        ...     \"\"\"Disable the robot arm.\"\"\"
    """

    def decorator(fn: Callable[..., Any]) -> Callable[..., _ResponseT]:
        method_name = fn.__name__

        @functools.wraps(fn)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> _ResponseT:
            delegate = getattr(self, target_attr)
            raw: str = getattr(delegate, method_name)(*args, **kwargs)
            return parse_response(raw, response_type)  # type: ignore[return-value]

        return wrapper

    return decorator
