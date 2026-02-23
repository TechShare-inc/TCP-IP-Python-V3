"""Typed response dataclasses and regex-based parser for Dobot TCP API responses.

The Dobot controller uses two text response formats over TCP:

* **3-field** ``"error_code,command_id,payload;"``
  e.g. ``"0,0,ok;"``

* **2-field** ``"error_code,{payload};"``
  e.g. ``"0,{5};"``  or  ``"0,{1001,1002};"``

:func:`parse_response` accepts both formats and returns a typed dataclass,
raising :class:`DobotApiError` when the controller signals a failure
(non-zero *error_code*) or when the response is malformed.

Typical usage (inside :class:`~dobot_api_v3.DobotRobot`)::

    raw = self.dashboard.robot_mode()
    return parse_response(raw, IntResponse)
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Tuple, Type, TypeVar

# ---------------------------------------------------------------------------
# Compiled regex — matches both 2-field and 3-field Dobot response formats.
#
#   3-field: "error_code,command_id,payload;"
#   2-field: "error_code,{brace_payload};"
#
# Named groups:
#   error_code  — always present; may be negative (e.g. -1)
#   cmd_id      — optional middle integer separated by commas on both sides
#   brace       — payload wrapped in {...}, stripped of the braces
#   plain       — plain-text payload (no braces), e.g. "ok"
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

# Helpers for payload value extraction (mirrors error_monitor.py convention).
_INT_RE = re.compile(r"-?\d+")
_FLOAT_RE = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?")


# ---------------------------------------------------------------------------
# Exception
# ---------------------------------------------------------------------------


class DobotApiError(Exception):
    """Raised when the Dobot controller returns a non-zero error code
    or when the response string cannot be parsed.

    Attributes:
        error_code: The integer error code from the response (negative for
            parse failures).
        command_id: The command queue ID from the response (0 when absent).
        message: Human-readable detail extracted from the payload.
        raw: The original response string received from the robot.
    """

    def __init__(
        self,
        error_code: int,
        command_id: int,
        message: str,
        raw: str,
    ) -> None:
        self.error_code = error_code
        self.command_id = command_id
        self.message = message
        self.raw = raw
        super().__init__(
            f"Dobot API error {error_code} (cmd_id={command_id}): "
            f"{message!r} [raw={raw!r}]"
        )


# ---------------------------------------------------------------------------
# Response dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AckResponse:
    """Simple acknowledgment response with no data payload.

    Returned by lifecycle commands (``enable_robot``, ``disable_robot``, …)
    and all motion commands (``mov_j``, ``sync``, …).

    Attributes:
        command_id: Motion-queue command ID from the controller (often 0).
    """

    command_id: int


@dataclass(frozen=True)
class IntResponse:
    """Single integer value response.

    Returned by status-query commands such as ``robot_mode``.

    Attributes:
        command_id: Motion-queue command ID from the controller.
        value: The integer value returned by the controller.
    """

    command_id: int
    value: int


@dataclass(frozen=True)
class PoseResponse:
    """Six-degree-of-freedom pose or joint-angle response.

    Returned by ``get_pose`` (Cartesian) and ``get_angle`` (joint).

    Attributes:
        command_id: Motion-queue command ID from the controller.
        x: X coordinate or joint-1 angle.
        y: Y coordinate or joint-2 angle.
        z: Z coordinate or joint-3 angle.
        rx: RX rotation or joint-4 angle.
        ry: RY rotation or joint-5 angle.
        rz: RZ rotation or joint-6 angle.
    """

    command_id: int
    x: float
    y: float
    z: float
    rx: float
    ry: float
    rz: float


@dataclass(frozen=True)
class ErrorIdResponse:
    """Alarm / error-ID list response.

    Returned by ``get_error_id``.  Zero sentinel values from the controller
    are filtered out, matching the behaviour of
    :class:`~dobot_api_v3.RobotErrorMonitor`.

    Attributes:
        command_id: Motion-queue command ID from the controller.
        error_ids: Tuple of non-zero alarm codes active on the controller.
    """

    command_id: int
    error_ids: Tuple[int, ...]


# ---------------------------------------------------------------------------
# TypeVar bound to all response types
# ---------------------------------------------------------------------------

_ResponseT = TypeVar(
    "_ResponseT", AckResponse, IntResponse, PoseResponse, ErrorIdResponse
)


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


def parse_response(raw: str, response_type: Type[_ResponseT]) -> _ResponseT:
    """Parse a raw Dobot TCP response string into a typed dataclass.

    Accepts both Dobot response formats:

    * ``"error_code,command_id,payload;"`` — 3-field plain
    * ``"error_code,{brace_payload};"`` — 2-field brace

    Args:
        raw: The raw response string received from the robot controller.
        response_type: The dataclass type to parse into.  Must be one of
            :class:`AckResponse`, :class:`IntResponse`,
            :class:`PoseResponse`, or :class:`ErrorIdResponse`.

    Returns:
        A populated, frozen response dataclass instance.

    Raises:
        DobotApiError: If the controller reports a non-zero error code, or
            if the response string is malformed / missing expected values.

    Example:
        >>> raw = dashboard.robot_mode()
        >>> resp = parse_response(raw, IntResponse)
        >>> print(resp.value)
        5
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

    # --- AckResponse ---
    if response_type is AckResponse:
        return AckResponse(command_id=command_id)  # type: ignore[return-value]

    # --- IntResponse ---
    if response_type is IntResponse:
        payload = brace_payload if brace_payload is not None else (plain_payload or "")
        ints = _INT_RE.findall(payload)
        if not ints:
            raise DobotApiError(
                error_code=0,
                command_id=command_id,
                message=f"expected integer payload, got: {payload!r}",
                raw=raw,
            )
        return IntResponse(command_id=command_id, value=int(ints[0]))  # type: ignore[return-value]

    # --- PoseResponse ---
    if response_type is PoseResponse:
        payload = brace_payload if brace_payload is not None else (plain_payload or "")
        floats = _FLOAT_RE.findall(payload)
        if len(floats) < 6:
            raise DobotApiError(
                error_code=0,
                command_id=command_id,
                message=f"expected 6 floats in pose payload, got: {payload!r}",
                raw=raw,
            )
        f = [float(v) for v in floats[:6]]
        return PoseResponse(  # type: ignore[return-value]
            command_id=command_id,
            x=f[0],
            y=f[1],
            z=f[2],
            rx=f[3],
            ry=f[4],
            rz=f[5],
        )

    # --- ErrorIdResponse ---
    if response_type is ErrorIdResponse:
        payload = brace_payload if brace_payload is not None else (plain_payload or "")
        all_ids = [int(v) for v in _INT_RE.findall(payload)]
        # Filter zero sentinel values — mirrors RobotErrorMonitor convention.
        error_ids = tuple(v for v in all_ids if v != 0)
        return ErrorIdResponse(command_id=command_id, error_ids=error_ids)  # type: ignore[return-value]

    raise TypeError(f"Unsupported response_type: {response_type!r}")  # pragma: no cover
