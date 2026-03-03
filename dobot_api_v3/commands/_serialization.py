"""Serialization helpers shared by all dashboard command mixins."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from ..utils import Pose

if TYPE_CHECKING:
    from typing import Protocol

    class _HasSendRecv(Protocol):
        """Structural contract: concrete class must supply ``send_recv_msg``."""

        def send_recv_msg(self, string: str) -> str:
            """Send one command and return the decoded reply."""
            ...

    _MixinBase = _HasSendRecv
else:
    _MixinBase = object

# ---------------------------------------------------------------------------
# Compiled regexes — duplicated from responses.py so the mixin layer does
# not depend on the response-dataclass module (which will be deprecated).
# ---------------------------------------------------------------------------

_RESPONSE_RE = re.compile(
    r"^(?P<error_code>-?\d+)"  # field 1: error code
    r","
    r"(?:(?P<cmd_id>\d+),)?"  # optional field 2: command_id (non-negative int)
    r"(?:\{(?P<brace>[^}]*)\}"  # either brace payload  {…}
    r"|(?P<plain>[^;]*)"  # or plain-text payload
    r");?$",
    re.ASCII,
)
_INT_RE = re.compile(r"-?\d+")
_FLOAT_RE = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?")


# ---------------------------------------------------------------------------
# Lightweight exception (re-exported from responses for compatibility)
# ---------------------------------------------------------------------------

from ..responses import DobotApiError  # noqa: E402


def _parse_raw(raw: str) -> tuple[int, int, str]:
    """Parse a raw Dobot TCP response into its three components.

    Args:
        raw: Raw response string from the robot controller.

    Returns:
        Tuple of ``(error_code, command_id, payload)``.

    Raises:
        DobotApiError: If the response is malformed or reports a non-zero
            error code.
    """
    m = _RESPONSE_RE.match(raw.strip())
    if m is None:
        raise DobotApiError(
            error_code=-1,
            command_id=0,
            message="malformed response",
            raw=raw,
        )

    error_code = int(m.group("error_code"))
    command_id = int(m.group("cmd_id") or "0")
    brace_payload: str | None = m.group("brace")
    plain_payload: str | None = m.group("plain")

    if error_code != 0:
        detail = brace_payload or plain_payload or ""
        raise DobotApiError(
            error_code=error_code,
            command_id=command_id,
            message=detail.strip(),
            raw=raw,
        )

    payload = brace_payload if brace_payload is not None else (plain_payload or "")
    return error_code, command_id, payload


class _SerializationMixin(_MixinBase):
    """Provides formatting, command-building, and response-parsing helpers.

    All ``_recv_*`` helpers call ``self.send_recv_msg``, which is **not**
    defined on this mixin at runtime.  It is provided by
    :class:`~dobot_api_v3.base.DobotApi` and reached naturally via the MRO
    of the concrete classes (:class:`~dobot_api_v3.commands.DobotApiDashboard`
    and :class:`~dobot_api_v3.commands.DobotApiMove`) where ``DobotApi``
    appears after all mixins::

        DobotApiDashboard → _SystemMixin → … → _SerializationMixin → DobotApi

    For static analysis, ``_MixinBase`` is bound to the ``_HasSendRecv``
    :class:`~typing.Protocol` under ``TYPE_CHECKING``, giving type checkers
    visibility of ``send_recv_msg`` without injecting a runtime stub that
    would shadow ``DobotApi.send_recv_msg`` in the MRO.
    """

    # ------------------------------------------------------------------ #
    # Response-parsing helpers                                             #
    # ------------------------------------------------------------------ #

    def _recv_ack(self, cmd: str) -> int:
        """Send *cmd* and return the command-queue ID from an ack response.

        Args:
            cmd: Serialized protocol command string.

        Returns:
            Command queue ID (often 0).
        """
        raw = self.send_recv_msg(cmd)
        _, command_id, _ = _parse_raw(raw)
        return command_id

    def _recv_int(self, cmd: str) -> int:
        """Send *cmd* and return a single integer from the payload.

        Args:
            cmd: Serialized protocol command string.

        Returns:
            The integer value extracted from the response payload.
        """
        raw = self.send_recv_msg(cmd)
        _, _, payload = _parse_raw(raw)
        ints = _INT_RE.findall(payload)
        if not ints:
            raise DobotApiError(
                error_code=0,
                command_id=0,
                message=f"expected integer payload, got: {payload!r}",
                raw=raw,
            )
        return int(ints[0])

    def _recv_pose(self, cmd: str) -> Pose:
        """Send *cmd* and return six floats from the brace payload.

        Args:
            cmd: Serialized protocol command string.

        Returns:
            Six-element tuple ``(v1, v2, v3, v4, v5, v6)``.
        """
        raw = self.send_recv_msg(cmd)
        _, _, payload = _parse_raw(raw)
        floats = _FLOAT_RE.findall(payload)
        if len(floats) < 6:
            raise DobotApiError(
                error_code=0,
                command_id=0,
                message=f"expected 6 floats, got: {payload!r}",
                raw=raw,
            )
        return (
            float(floats[0]),
            float(floats[1]),
            float(floats[2]),
            float(floats[3]),
            float(floats[4]),
            float(floats[5]),
        )

    def _recv_error_ids(self, cmd: str) -> tuple[int, ...]:
        """Send *cmd* and return non-zero alarm IDs from the payload.

        Args:
            cmd: Serialized protocol command string.

        Returns:
            Tuple of non-zero alarm codes (may be empty).
        """
        raw = self.send_recv_msg(cmd)
        _, _, payload = _parse_raw(raw)
        all_ids = [int(v) for v in _INT_RE.findall(payload)]
        return tuple(v for v in all_ids if v != 0)

    def _recv_int_list(self, cmd: str) -> tuple[int, ...]:
        """Send *cmd* and return all integers from the brace payload.

        Args:
            cmd: Serialized protocol command string.

        Returns:
            Tuple of integers extracted from the response.
        """
        raw = self.send_recv_msg(cmd)
        _, _, payload = _parse_raw(raw)
        return tuple(int(v) for v in _INT_RE.findall(payload))

    def _recv_float_list(self, cmd: str) -> tuple[float, ...]:
        """Send *cmd* and return all floats from the brace payload.

        Args:
            cmd: Serialized protocol command string.

        Returns:
            Tuple of floats extracted from the response.
        """
        raw = self.send_recv_msg(cmd)
        _, _, payload = _parse_raw(raw)
        return tuple(float(v) for v in _FLOAT_RE.findall(payload))

    def _recv_str_list(self, cmd: str) -> tuple[str, ...]:
        """Send *cmd* and return comma-separated tokens from the payload.

        Args:
            cmd: Serialized protocol command string.

        Returns:
            Tuple of stripped string tokens.
        """
        raw = self.send_recv_msg(cmd)
        _, _, payload = _parse_raw(raw)
        if not payload.strip():
            return ()
        return tuple(tok.strip() for tok in payload.split(","))

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
