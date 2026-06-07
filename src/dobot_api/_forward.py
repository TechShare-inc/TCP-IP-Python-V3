"""Decorator for forwarding DobotRobot methods to sub-objects."""

from __future__ import annotations

import functools
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def forward_to(
    delegate_method: Callable[..., Any],
    *,
    target_attr: str = "dashboard",
    return_type: type | None = None,
) -> Callable[[F], F]:
    """Forward a facade method call to a named delegate attribute."""
    method_name = delegate_method.__name__

    def decorator(method: F) -> F:
        @functools.wraps(method)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            target = getattr(self, target_attr)
            return getattr(target, method_name)(*args, **kwargs)

        wrapper.__forward_target__ = target_attr  # type: ignore[attr-defined]
        wrapper.__forward_method__ = method_name  # type: ignore[attr-defined]
        if return_type is not None:
            wrapper.__forward_return_type__ = return_type  # type: ignore[attr-defined]
        return wrapper  # type: ignore[return-value]

    return decorator

__all__ = ["forward_to"]
