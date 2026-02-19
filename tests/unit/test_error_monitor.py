"""Unit tests for RobotErrorMonitor — alarm query, parsing, and clear."""

from __future__ import annotations

import time as time_mod
from unittest.mock import MagicMock, patch

import pytest

from dobot_api_v3.error_monitor import RobotErrorMonitor

pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def monitor() -> RobotErrorMonitor:
    """RobotErrorMonitor with no active connection."""
    return RobotErrorMonitor(robot_ip="192.168.1.1", dashboard_port=29999)


@pytest.fixture
def connected_monitor(
    monitor: RobotErrorMonitor,
) -> RobotErrorMonitor:
    """RobotErrorMonitor with a mock dashboard already injected."""
    mock_db = MagicMock()
    monitor.dashboard = mock_db
    return monitor


# ---------------------------------------------------------------------------
# connect / disconnect
# ---------------------------------------------------------------------------


class TestConnect:
    def test_connect_creates_dashboard(
        self, monitor: RobotErrorMonitor, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_cls = MagicMock()
        monkeypatch.setattr(
            "dobot_api_v3.error_monitor.DobotApiDashboard", mock_cls
        )
        result = monitor.connect()
        assert result is True
        mock_cls.assert_called_once_with("192.168.1.1", 29999)
        assert monitor.dashboard is not None

    def test_connect_returns_false_on_exception(
        self, monitor: RobotErrorMonitor, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "dobot_api_v3.error_monitor.DobotApiDashboard",
            MagicMock(side_effect=ConnectionError("refused")),
        )
        result = monitor.connect()
        assert result is False

    def test_disconnect_calls_close_on_dashboard(
        self, connected_monitor: RobotErrorMonitor
    ) -> None:
        connected_monitor.disconnect()
        connected_monitor.dashboard.close.assert_called_once()  # type: ignore[union-attr]


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
        connected_monitor: RobotErrorMonitor,
        response: str,
        expected_ids: list,
    ) -> None:
        connected_monitor.dashboard.get_error_id.return_value = response  # type: ignore[union-attr]
        result = connected_monitor.get_error_info("en")
        assert result is not None
        ids = [e["id"] for e in result["errMsg"]]
        assert ids == expected_ids

    def test_returns_none_when_not_connected(self, monitor: RobotErrorMonitor) -> None:
        result = monitor.get_error_info()
        assert result is None

    def test_uses_snake_case_get_error_id(
        self, connected_monitor: RobotErrorMonitor
    ) -> None:
        """Must call get_error_id() not the deprecated GetErrorID()."""
        connected_monitor.dashboard.get_error_id.return_value = "0,{0};"  # type: ignore[union-attr]
        connected_monitor.get_error_info("en")
        connected_monitor.dashboard.get_error_id.assert_called_once()  # type: ignore[union-attr]
        connected_monitor.dashboard.GetErrorID.assert_not_called()  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# clear_robot_error
# ---------------------------------------------------------------------------


class TestClearRobotError:
    def test_calls_snake_case_clear_error(
        self, connected_monitor: RobotErrorMonitor
    ) -> None:
        """Must call clear_error() not the deprecated ClearError()."""
        connected_monitor.dashboard.get_error_id.return_value = "0,{1001};"  # type: ignore[union-attr]
        connected_monitor.dashboard.clear_error.return_value = "0,0,ok;"  # type: ignore[union-attr]
        connected_monitor.clear_robot_error("en")
        connected_monitor.dashboard.clear_error.assert_called()  # type: ignore[union-attr]
        connected_monitor.dashboard.ClearError.assert_not_called()  # type: ignore[union-attr]

    def test_returns_false_when_not_connected(self, monitor: RobotErrorMonitor) -> None:
        assert monitor.clear_robot_error() is False

    def test_returns_false_when_no_errors(
        self, connected_monitor: RobotErrorMonitor
    ) -> None:
        connected_monitor.dashboard.get_error_id.return_value = "0,{0};"  # type: ignore[union-attr]
        result = connected_monitor.clear_robot_error("en")
        assert result is False


# ---------------------------------------------------------------------------
# check_errors
# ---------------------------------------------------------------------------


class TestCheckErrors:
    def test_returns_false_when_no_errors(
        self, connected_monitor: RobotErrorMonitor
    ) -> None:
        connected_monitor.dashboard.get_error_id.return_value = "0,{0};"  # type: ignore[union-attr]
        assert connected_monitor.check_errors("en") is False

    def test_returns_true_when_errors_present(
        self, connected_monitor: RobotErrorMonitor
    ) -> None:
        connected_monitor.dashboard.get_error_id.return_value = "0,{1001};"  # type: ignore[union-attr]
        assert connected_monitor.check_errors("en") is True


# ---------------------------------------------------------------------------
# monitor_errors — infinite loop interrupted by KeyboardInterrupt
# ---------------------------------------------------------------------------


class TestMonitorErrors:
    def test_loops_until_keyboard_interrupt(
        self, connected_monitor: RobotErrorMonitor, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        connected_monitor.dashboard.get_error_id.return_value = "0,{0};"  # type: ignore[union-attr]
        call_count = 0

        def fake_sleep(interval: float) -> None:
            nonlocal call_count
            call_count += 1
            if call_count >= 3:
                raise KeyboardInterrupt

        monkeypatch.setattr(time_mod, "sleep", fake_sleep)
        connected_monitor.monitor_errors(interval=1, language="en")
        assert call_count == 3
