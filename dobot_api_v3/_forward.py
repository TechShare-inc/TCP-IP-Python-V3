"""Decorator for forwarding DobotRobot methods to sub-objects.

Usage::

    from dobot_api_v3._forward import forward_to
    from dobot_api_v3.commands.dashboard import DobotApiDashboard

    class DobotRobot:
        @forward_to(DobotApiDashboard.disable_robot)
        def disable_robot(self) -> int:
            \"\"\"Disable the robot arm.\"\"\"

The decorator replaces the method body with a delegation to
``self.<target_attr>.<method_name>(*args, **kwargs)`` whose result
is returned unchanged.

The original signature and docstring are preserved via :func:`functools.wraps`
so that IDEs and type-checkers still see the correct interface.
"""

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
    """Decorator that forwards a DobotRobot method call to a delegate.

    At decoration time the decorator captures *delegate_method.__name__*
    so the wrapper knows which delegate method to call at runtime.

    The decorated method's body (conventionally ``...``) is **never
    executed**.  The wrapper calls
    ``self.<target_attr>.<method_name>(*args, **kwargs)`` and returns the
    result unchanged.

    Args:
        delegate_method: The unbound method on the delegate class (e.g.
            ``DobotApiDashboard.enable_robot``).  Used only to derive
            the method name — it is not called directly.
        target_attr: Name of the instance attribute that holds the delegate
            object (e.g. ``"dashboard"`` or ``"move"``).
        return_type: Optional type metadata stored on the wrapper as
            ``__forward_return_type__`` for introspection and
            documentation tooling.  Not used at runtime.

    Returns:
        A decorator that replaces *method* with a forwarding wrapper
        while preserving its docstring, annotations, and signature.
    """
    method_name: str = delegate_method.__name__

    def decorator(method: F) -> F:
        @functools.wraps(method)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            target = getattr(self, target_attr)
            return getattr(target, method_name)(*args, **kwargs)

        # Attach metadata for introspection / documentation tooling.
        wrapper.__forward_target__ = target_attr  # type: ignore[attr-defined]
        wrapper.__forward_method__ = method_name  # type: ignore[attr-defined]
        if return_type is not None:
            wrapper.__forward_return_type__ = return_type  # type: ignore[attr-defined]

        return wrapper  # type: ignore[return-value]

    return decorator
