"""Serialization helpers shared by all dashboard command mixins."""

from __future__ import annotations


class _SerializationMixin:
    """Provides ``_fmt`` and ``_build_cmd`` helpers for Dobot protocol commands.

    This mixin also declares a ``send_recv_msg`` stub so that type checkers
    see the method on all dashboard mixins (the real implementation is
    provided by :class:`~dobot_api_v3.base.DobotApi` through Python MRO at
    runtime).
    """

    # ------------------------------------------------------------------ #
    # Runtime stub — overridden by DobotApi in the final MRO.             #
    # ------------------------------------------------------------------ #

    def send_recv_msg(self, string: str) -> str:  # pragma: no cover
        """Provided by DobotApi via MRO; not called directly on mixin."""
        raise NotImplementedError("Provided by DobotApi via MRO")

    # ------------------------------------------------------------------ #
    # Formatting helpers                                                   #
    # ------------------------------------------------------------------ #

    def _fmt(self, value: int | float | str | list | tuple) -> str:  # type: ignore[return]
        """Format one command argument into Dobot protocol text.

        Args:
            value: Scalar or collection argument value.

        Returns:
            Protocol-ready string representation.
        """
        if isinstance(value, (list, tuple)):
            return "{" + ",".join(self._fmt(item) for item in value) + "}"
        if isinstance(value, float):
            return "{:f}".format(value)
        if isinstance(value, int):
            return "{:d}".format(value)
        return str(value)

    def _build_cmd(
        self, name: str, *args: int | float | str, **kwargs: int | float | str
    ) -> str:
        """Build a Dobot protocol command string.

        Args:
            name: Protocol command name.
            *args: Positional command arguments.
            **kwargs: Keyword-style command arguments (``key=value`` form).

        Returns:
            Serialized command text, e.g. ``"SpeedFactor(40)"``.
        """
        parts = [self._fmt(item) for item in args]
        parts.extend(f"{k}={self._fmt(v)}" for k, v in kwargs.items())
        return f"{name}(" + ",".join(parts) + ")"
