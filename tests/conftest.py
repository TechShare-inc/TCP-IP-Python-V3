"""Shared pytest fixtures for dobot_api_v3 tests."""

from __future__ import annotations

from typing import Callable
from unittest.mock import MagicMock

import numpy as np
import pytest

from dobot_api_v3.base import DobotApi, FeedbackDtype
from dobot_api_v3.dashboard import DobotApiDashboard
from dobot_api_v3.feedback import DobotApiFeedback
from dobot_api_v3.move import DobotApiMove


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
        return f"0,0,{cmd};"

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
        return f"0,0,{cmd};"

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
