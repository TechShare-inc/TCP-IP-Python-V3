"""Unit tests — all PascalCase deprecated aliases emit DeprecationWarning."""

from __future__ import annotations

import warnings
from unittest.mock import MagicMock

import pytest

from dobot_api_v3.base import DobotApi, FeedbackDtype, MyType
from dobot_api_v3.dashboard import DobotApiDashboard
from dobot_api_v3.feedback import DobotApiFeedBack, DobotApiFeedback
from dobot_api_v3.move import DobotApiMove

pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_dashboard(monkeypatch: pytest.MonkeyPatch) -> DobotApiDashboard:
    monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
    db = DobotApiDashboard("127.0.0.1", 29999)
    db.socket_dobot = MagicMock()
    db.socket_dobot.recv.return_value = b"0,0,ok;"
    return db


def _make_move(monkeypatch: pytest.MonkeyPatch) -> DobotApiMove:
    monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
    mv = DobotApiMove("127.0.0.1", 30003)
    mv.socket_dobot = MagicMock()
    mv.socket_dobot.recv.return_value = b"0,0,ok;"
    return mv


def _has_dep_warning(w: list[warnings.WarningMessage], name: str) -> bool:
    return any(
        issubclass(x.category, DeprecationWarning) and name in str(x.message) for x in w
    )


# ---------------------------------------------------------------------------
# Dashboard aliases
# ---------------------------------------------------------------------------


_DASHBOARD_ALIASES = [
    ("EnableRobot", lambda db: db.EnableRobot()),
    ("DisableRobot", lambda db: db.DisableRobot()),
    ("ClearError", lambda db: db.ClearError()),
    ("ResetRobot", lambda db: db.ResetRobot()),
    ("SpeedFactor", lambda db: db.SpeedFactor(50)),
    ("RobotMode", lambda db: db.RobotMode()),
    ("GetAngle", lambda db: db.GetAngle()),
    ("GetPose", lambda db: db.GetPose()),
    ("EmergencyStop", lambda db: db.EmergencyStop()),
    ("GetErrorID", lambda db: db.GetErrorID()),
    ("PowerOn", lambda db: db.PowerOn()),
    ("StopScript", lambda db: db.StopScript()),
    ("PauseScript", lambda db: db.PauseScript()),
    ("ContinueScript", lambda db: db.ContinueScript()),
    ("GetSixForceData", lambda db: db.GetSixForceData()),
    ("GetTerminal485", lambda db: db.GetTerminal485()),
    ("TCPSpeedEnd", lambda db: db.TCPSpeedEnd()),
    ("StartDrag", lambda db: db.StartDrag()),
    ("StopDrag", lambda db: db.StopDrag()),
    ("Continue", lambda db: db.Continue()),
]


@pytest.mark.parametrize("alias,call_fn", _DASHBOARD_ALIASES)
def test_dashboard_alias_emits_deprecation_warning(
    alias: str,
    call_fn: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    db = _make_dashboard(monkeypatch)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        call_fn(db)  # type: ignore[operator]
    assert _has_dep_warning(
        w, alias
    ), f"Expected DeprecationWarning mentioning '{alias}' but got: " + str(
        [str(x.message) for x in w]
    )


# ---------------------------------------------------------------------------
# Move aliases
# ---------------------------------------------------------------------------


_MOVE_ALIASES = [
    ("MovJ", lambda mv: mv.MovJ(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)),
    ("MovL", lambda mv: mv.MovL(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)),
    ("JointMovJ", lambda mv: mv.JointMovJ(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)),
    ("RelMovJ", lambda mv: mv.RelMovJ(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)),
    ("RelMovL", lambda mv: mv.RelMovL(0.0, 0.0, 0.0)),
    ("Sync", lambda mv: mv.Sync()),
    ("ServoJS", lambda mv: mv.ServoJS(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)),
    ("ServoP", lambda mv: mv.ServoP(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)),
]


@pytest.mark.parametrize("alias,call_fn", _MOVE_ALIASES)
def test_move_alias_emits_deprecation_warning(
    alias: str,
    call_fn: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mv = _make_move(monkeypatch)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        call_fn(mv)  # type: ignore[operator]
    assert _has_dep_warning(
        w, alias
    ), f"Expected DeprecationWarning mentioning '{alias}' but got: " + str(
        [str(x.message) for x in w]
    )


# ---------------------------------------------------------------------------
# Module-level deprecated names
# ---------------------------------------------------------------------------


def test_my_type_is_identical_to_feedback_dtype() -> None:
    """MyType must be the same object as FeedbackDtype (not a copy)."""
    assert MyType is FeedbackDtype


def test_dobot_api_feedback_back_is_feedback_class_alias() -> None:
    """DobotApiFeedBack must point to DobotApiFeedback."""
    assert DobotApiFeedBack is DobotApiFeedback
