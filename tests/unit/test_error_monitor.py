"""Unit tests for RobotErrorMonitor — alarm query, parsing, and clear."""

from __future__ import annotations

import time as time_mod
import warnings
from unittest.mock import MagicMock, patch

import pytest

from dobot_api_v3.error_monitor import RobotErrorMonitor

pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def monitor() -> RobotErrorMonitor:
    """RobotErrorMonitor with a mock dashboard injected."""
    return RobotErrorMonitor(dashboard=MagicMock())


# ---------------------------------------------------------------------------
# Deprecated helpers: connect / disconnect / from_connection
# ---------------------------------------------------------------------------


class TestDeprecatedHelpers:
    def test_connect_is_noop_and_warns(self, monitor: RobotErrorMonitor) -> None:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = monitor.connect()
        assert result is True
        assert any(issubclass(w.category, DeprecationWarning) for w in caught)

    def test_disconnect_is_noop_and_warns(self, monitor: RobotErrorMonitor) -> None:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            monitor.disconnect()
        assert any(issubclass(w.category, DeprecationWarning) for w in caught)
        # Dashboard must NOT have been closed — caller owns lifecycle.
        monitor.dashboard.close.assert_not_called()  # type: ignore[union-attr]

    def test_from_connection_warns_and_returns_monitor(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_cls = MagicMock()
        monkeypatch.setattr("dobot_api_v3.error_monitor.DobotApiDashboard", mock_cls)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            m = RobotErrorMonitor.from_connection("192.168.1.1", 29999)
        mock_cls.assert_called_once_with("192.168.1.1", 29999)
        assert isinstance(m, RobotErrorMonitor)
        assert any(issubclass(w.category, DeprecationWarning) for w in caught)


# ---------------------------------------------------------------------------
# get_error_info — response parsing
# ---------------------------------------------------------------------------


class TestGetErrorInfo:
    @pytest.mark.parametrize(
        "response,expected_ids",
        [
            # Protocol response: "0,{1001,0};" → codes are [0, 1, 0, 0, 1] or similar
            # We test the regex r"-?\d+" extraction directly.
            ("0,{0};", []),  # only error_id=0 → filtered out
            ("0,{1001,0};", [1001]),  # 1001 is non-zero, 0 is filtered
            ("0,{1001,1002};", [1001, 1002]),
            ("0,{-1,2};", [-1, 2]),  # negative IDs included
            ("", []),  # empty response
        ],
    )
    def test_error_code_extraction(
        self,
        monitor: RobotErrorMonitor,
        response: str,
        expected_ids: list,
    ) -> None:
        monitor.dashboard.get_error_id.return_value = response  # type: ignore[union-attr]
        result = monitor.get_error_info("en")
        assert result is not None
        ids = [e["id"] for e in result["errMsg"]]
        assert ids == expected_ids

    def test_uses_snake_case_get_error_id(
        self, monitor: RobotErrorMonitor
    ) -> None:
        """Must call get_error_id() not the deprecated GetErrorID()."""
        monitor.dashboard.get_error_id.return_value = "0,{0};"  # type: ignore[union-attr]
        monitor.get_error_info("en")
        monitor.dashboard.get_error_id.assert_called_once()  # type: ignore[union-attr]
        monitor.dashboard.GetErrorID.assert_not_called()  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# clear_robot_error
# ---------------------------------------------------------------------------


class TestClearRobotError:
    def test_calls_snake_case_clear_error(
        self, monitor: RobotErrorMonitor
    ) -> None:
        """Must call clear_error() not the deprecated ClearError()."""
        monitor.dashboard.get_error_id.return_value = "0,{1001};"  # type: ignore[union-attr]
        monitor.dashboard.clear_error.return_value = "0,0,ok;"  # type: ignore[union-attr]
        monitor.clear_robot_error("en")
        monitor.dashboard.clear_error.assert_called()  # type: ignore[union-attr]
        monitor.dashboard.ClearError.assert_not_called()  # type: ignore[union-attr]

    def test_returns_false_when_no_errors(
        self, monitor: RobotErrorMonitor
    ) -> None:
        monitor.dashboard.get_error_id.return_value = "0,{0};"  # type: ignore[union-attr]
        result = monitor.clear_robot_error("en")
        assert result is False


# ---------------------------------------------------------------------------
# check_errors
# ---------------------------------------------------------------------------


class TestCheckErrors:
    def test_returns_false_when_no_errors(
        self, monitor: RobotErrorMonitor
    ) -> None:
        monitor.dashboard.get_error_id.return_value = "0,{0};"  # type: ignore[union-attr]
        assert monitor.check_errors("en") is False

    def test_returns_true_when_errors_present(
        self, monitor: RobotErrorMonitor
    ) -> None:
        monitor.dashboard.get_error_id.return_value = "0,{1001};"  # type: ignore[union-attr]
        assert monitor.check_errors("en") is True


# ---------------------------------------------------------------------------
# monitor_errors — infinite loop interrupted by KeyboardInterrupt
# ---------------------------------------------------------------------------


class TestMonitorErrors:
    def test_loops_until_keyboard_interrupt(
        self, monitor: RobotErrorMonitor, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monitor.dashboard.get_error_id.return_value = "0,{0};"  # type: ignore[union-attr]
        call_count = 0

        def fake_sleep(interval: float) -> None:
            nonlocal call_count
            call_count += 1
            if call_count >= 3:
                raise KeyboardInterrupt

        monkeypatch.setattr(time_mod, "sleep", fake_sleep)
        monitor.monitor_errors(interval=1, language="en")
        assert call_count == 3
