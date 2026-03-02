"""Shared pytest fixtures for dobot_api_v3 tests."""

from __future__ import annotations

import re
from typing import Callable
from unittest.mock import MagicMock

import numpy as np
import pytest

from dobot_api_v3.base import DobotApi, FeedbackDtype
from dobot_api_v3.dashboard import DobotApiDashboard
from dobot_api_v3.feedback import DobotApiFeedback
from dobot_api_v3.move import DobotApiMove

# ---------------------------------------------------------------------------
# Mock response routing — maps command prefixes to realistic response strings
# so that _recv_int / _recv_pose / etc. don't crash in serialization tests.
# ---------------------------------------------------------------------------

# Commands whose response carries a single integer in brace payload.
_INT_COMMANDS = {"RobotMode", "DI", "ToolDI", "ModbusCreate"}

# Commands whose response carries six floats (pose / angle / force).
_POSE_COMMANDS = {
    "GetAngle",
    "GetPose",
    "GetSixForceData",
    "GetTraceStartPose",
    "GetPathStartPose",
    "PositiveSolution",
    "InverseSolution",
}

# Commands whose response carries an int list (coils, bits).
_INT_LIST_COMMANDS = {"GetCoils", "GetInBits"}

# Commands whose response carries a float list (registers).
_FLOAT_LIST_COMMANDS = {"GetHoldRegs", "GetInRegs"}

# Commands whose response carries error IDs.
_ERROR_ID_COMMANDS = {"GetErrorID"}

# Commands whose response carries a comma-separated string list.
_STR_LIST_COMMANDS = {"GetTerminal485"}

_CMD_PREFIX_RE = re.compile(r"^(\w+)\(")


def _mock_response(cmd: str) -> str:
    """Return a realistic mock response string for *cmd*.

    The response is chosen based on the protocol command prefix so that
    the ``_recv_*`` helpers in ``_SerializationMixin`` parse successfully.
    """
    m = _CMD_PREFIX_RE.match(cmd)
    prefix = m.group(1) if m else ""

    if prefix in _INT_COMMANDS:
        return "0,{0};"
    if prefix in _POSE_COMMANDS:
        return "0,{0.0,0.0,0.0,0.0,0.0,0.0};"
    if prefix in _INT_LIST_COMMANDS:
        return "0,{0};"
    if prefix in _FLOAT_LIST_COMMANDS:
        return "0,{0.0};"
    if prefix in _ERROR_ID_COMMANDS:
        return "0,{0};"
    if prefix in _STR_LIST_COMMANDS:
        return "0,{9600,8,N,1};"
    # Default: 3-field ack response.
    return "0,0,ok;"


# ---------------------------------------------------------------------------
# Base API fixture — socket fully mocked, send_recv_msg untouched.
# Use this when testing the networking layer itself (send_data, wait_reply, etc.)
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_base(monkeypatch: pytest.MonkeyPatch) -> DobotApi:
    """DobotApi instance with _connect patched out and a MagicMock socket."""
    monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
    api = DobotApi("192.168.1.1", 29999)
    api.socket_dobot = MagicMock()
    return api


# ---------------------------------------------------------------------------
# Dashboard fixture — send_recv_msg is intercepted to capture command strings.
# Use this when testing command serialization (no real networking).
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_dashboard(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[DobotApiDashboard, list[str]]:
    """DobotApiDashboard with send_recv_msg captured; returns (dashboard, sent_commands)."""
    monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
    db = DobotApiDashboard("192.168.1.1", 29999)
    db.socket_dobot = MagicMock()

    sent: list[str] = []

    def _capture(cmd: str) -> str:
        sent.append(cmd)
        return _mock_response(cmd)

    monkeypatch.setattr(db, "send_recv_msg", _capture)
    return db, sent


# ---------------------------------------------------------------------------
# Move fixture — same pattern as mock_dashboard.
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_move(monkeypatch: pytest.MonkeyPatch) -> tuple[DobotApiMove, list[str]]:
    """DobotApiMove with send_recv_msg captured; returns (move, sent_commands)."""
    monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
    mv = DobotApiMove("192.168.1.1", 30003)
    mv.socket_dobot = MagicMock()

    sent: list[str] = []

    def _capture(cmd: str) -> str:
        sent.append(cmd)
        return _mock_response(cmd)

    monkeypatch.setattr(mv, "send_recv_msg", _capture)
    return mv, sent


# ---------------------------------------------------------------------------
# Feedback fixture — _connect patched, socket.recv returns configurable data.
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_feedback(monkeypatch: pytest.MonkeyPatch) -> DobotApiFeedback:
    """DobotApiFeedback with _connect patched out and a MagicMock socket."""
    monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
    fb = DobotApiFeedback("192.168.1.1", 30004)
    fb.socket_dobot = MagicMock()
    return fb


# ---------------------------------------------------------------------------
# Feedback buffer factory — builds valid 1440-byte buffers for feedback tests.
# ---------------------------------------------------------------------------


@pytest.fixture
def feedback_buffer_factory() -> Callable[..., bytes]:
    """Returns a factory: call with field=value kwargs to get a 1440-byte bytes object.

    Example::

        buf = feedback_buffer_factory(robot_mode=5, load=1.5)
    """

    def factory(**kwargs: object) -> bytes:
        arr = np.zeros(1, dtype=FeedbackDtype)
        for field, value in kwargs.items():
            arr[0][field] = value  # type: ignore[index]
        raw = arr.tobytes()
        assert len(raw) == 1440, f"FeedbackDtype size mismatch: {len(raw)} != 1440"
        return raw

    return factory
