"""Utility helpers for Dobot API."""

from __future__ import annotations

import functools
import warnings
from typing import Any, Callable, Union

# ---------------------------------------------------------------------------
# Variadic parameter type aliases used by move/dashboard command methods.
# ---------------------------------------------------------------------------

# Pattern A — Generic dynamic parameters converted via str().
# Callers may pass individual ints, floats, strings, or tuples/lists that
# will be serialised as-is into the TCP command string.
DynParam = Union[int, float, str, tuple]  # type: ignore[type-arg]

# Pattern B — Structured (speed, acc, coord_index) tuples expected by
# RelMovJTool and RelMovLTool when optional parameters are provided.
ToolDynParam = tuple[int, int, int]


# ---------------------------------------------------------------------------
# Deprecation helper.
# ---------------------------------------------------------------------------


def deprecated_alias(
    new_name: str,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator that marks a method as a deprecated alias for *new_name*.

    Usage (inside a class body)::

        @deprecated_alias("enable_robot")
        def EnableRobot(self, *args, **kwargs):
            return self.enable_robot(*args, **kwargs)

    At call time the decorator emits a ``DeprecationWarning`` pointing at the
    caller's frame and then delegates to the wrapped function body.
    """

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        old_name = fn.__qualname__.split(".")[-1]

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(
                f"{old_name} is deprecated, use {new_name} instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            return fn(*args, **kwargs)

        return wrapper

    return decorator
