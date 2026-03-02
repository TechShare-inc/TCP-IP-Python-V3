"""Unit tests for RobotErrorMonitor — alarm query, parsing, and clear.

The dashboard methods called by RobotErrorMonitor now return parsed Python
types (``tuple[int, ...]`` for ``get_error_id()``, ``int`` for
``clear_error()``) rather than raw response strings.  All mocks in this
module reflect those return types.
"""

from __future__ import annotations

import time as time_mod
from unittest.mock import MagicMock

import pytest

from dobot_api_v3.error_monitor import RobotErrorMonitor

pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_dashboard() -> MagicMock:
    """MagicMock standing in for DobotApiDashboard."""
    return MagicMock()


@pytest.fixture
def monitor(mock_dashboard: MagicMock) -> RobotErrorMonitor:
    """RobotErrorMonitor with a mock dashboard injected."""
    return RobotErrorMonitor(dashboard=mock_dashboard)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# get_error_info — processes parsed error codes from dashboard
# ---------------------------------------------------------------------------


class TestGetErrorInfo:
    @pytest.mark.parametrize(
        "error_codes,expected_ids",
        [
            # get_error_id() returns tuple[int, ...] with zeros already
            # filtered by _recv_error_ids.  get_error_info additionally
            # skips any remaining 0s in its own loop.
            ((), []),  # no errors
            ((1001,), [1001]),  # single alarm
            ((1001, 1002), [1001, 1002]),  # multiple alarms
            ((-1, 2), [-1, 2]),  # negative IDs preserved
            ((0,), []),  # zero filtered by get_error_info loop
        ],
    )
    def test_error_code_extraction(
        self,
        monitor: RobotErrorMonitor,
        mock_dashboard: MagicMock,
        error_codes: tuple[int, ...],
        expected_ids: list[int],
    ) -> None:
        mock_dashboard.get_error_id.return_value = error_codes
        result = monitor.get_error_info("en")
        assert result is not None
        ids = [e["id"] for e in result["errMsg"]]
        assert ids == expected_ids

    def test_returns_empty_err_msg_when_no_errors(
        self, monitor: RobotErrorMonitor, mock_dashboard: MagicMock
    ) -> None:
        mock_dashboard.get_error_id.return_value = ()
        result = monitor.get_error_info("en")
        assert result == {"errMsg": []}

    def test_alarm_dict_contains_required_keys(
        self, monitor: RobotErrorMonitor, mock_dashboard: MagicMock
    ) -> None:
        """Each alarm entry must contain the standard i18n keys."""
        mock_dashboard.get_error_id.return_value = (1001,)
        result = monitor.get_error_info("en")
        assert result is not None
        alarm = result["errMsg"][0]
        for key in ("id", "type", "description", "cause", "solution", "level"):
            assert key in alarm, f"Missing key: {key}"

    def test_uses_snake_case_get_error_id(
        self, monitor: RobotErrorMonitor, mock_dashboard: MagicMock
    ) -> None:
        """Must call get_error_id() not the deprecated GetErrorID()."""
        mock_dashboard.get_error_id.return_value = ()
        monitor.get_error_info("en")
        mock_dashboard.get_error_id.assert_called_once()
        mock_dashboard.GetErrorID.assert_not_called()

    def test_returns_none_on_exception(
        self, monitor: RobotErrorMonitor, mock_dashboard: MagicMock
    ) -> None:
        """get_error_info returns None when an unexpected exception occurs."""
        mock_dashboard.get_error_id.side_effect = RuntimeError("network error")
        result = monitor.get_error_info("en")
        assert result is None

    def test_sets_language_before_querying(
        self, monitor: RobotErrorMonitor, mock_dashboard: MagicMock
    ) -> None:
        """The requested language must be applied before alarm lookup."""
        mock_dashboard.get_error_id.return_value = (1001,)
        monitor.get_error_info("zh_CN")
        assert monitor.i18n.get_current_language() == "zh_CN"


# ---------------------------------------------------------------------------
# clear_robot_error
# ---------------------------------------------------------------------------


class TestClearRobotError:
    def test_calls_snake_case_clear_error(
        self, monitor: RobotErrorMonitor, mock_dashboard: MagicMock
    ) -> None:
        """Must call clear_error() not the deprecated ClearError()."""
        mock_dashboard.get_error_id.return_value = (1001,)
        mock_dashboard.clear_error.return_value = 0
        monitor.clear_robot_error("en")
        mock_dashboard.clear_error.assert_called()
        mock_dashboard.ClearError.assert_not_called()

    def test_returns_false_when_no_errors(
        self, monitor: RobotErrorMonitor, mock_dashboard: MagicMock
    ) -> None:
        mock_dashboard.get_error_id.return_value = ()
        result = monitor.clear_robot_error("en")
        assert result is False

    def test_returns_true_when_errors_cleared(
        self, monitor: RobotErrorMonitor, mock_dashboard: MagicMock
    ) -> None:
        mock_dashboard.get_error_id.return_value = (1001,)
        mock_dashboard.clear_error.return_value = 0
        result = monitor.clear_robot_error("en")
        assert result is True

    def test_returns_false_on_exception(
        self, monitor: RobotErrorMonitor, mock_dashboard: MagicMock
    ) -> None:
        """Returns False (not raises) when clear_error itself fails."""
        mock_dashboard.get_error_id.return_value = (1001,)
        mock_dashboard.clear_error.side_effect = RuntimeError("timeout")
        result = monitor.clear_robot_error("en")
        assert result is False


# ---------------------------------------------------------------------------
# check_errors
# ---------------------------------------------------------------------------


class TestCheckErrors:
    def test_returns_false_when_no_errors(
        self, monitor: RobotErrorMonitor, mock_dashboard: MagicMock
    ) -> None:
        mock_dashboard.get_error_id.return_value = ()
        assert monitor.check_errors("en") is False

    def test_returns_true_when_errors_present(
        self, monitor: RobotErrorMonitor, mock_dashboard: MagicMock
    ) -> None:
        mock_dashboard.get_error_id.return_value = (1001,)
        assert monitor.check_errors("en") is True

    def test_returns_false_when_get_error_info_returns_none(
        self, monitor: RobotErrorMonitor, mock_dashboard: MagicMock
    ) -> None:
        """Covers the branch where get_error_info fails and returns None."""
        mock_dashboard.get_error_id.side_effect = RuntimeError("fail")
        assert monitor.check_errors("en") is False


# ---------------------------------------------------------------------------
# monitor_errors — infinite loop interrupted by KeyboardInterrupt
# ---------------------------------------------------------------------------


class TestMonitorErrors:
    def test_loops_until_keyboard_interrupt(
        self,
        monitor: RobotErrorMonitor,
        mock_dashboard: MagicMock,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        mock_dashboard.get_error_id.return_value = ()
        call_count = 0

        def fake_sleep(interval: float) -> None:
            nonlocal call_count
            call_count += 1
            if call_count >= 3:
                raise KeyboardInterrupt

        monkeypatch.setattr(time_mod, "sleep", fake_sleep)
        monitor.monitor_errors(interval=1, language="en")
        assert call_count == 3


# ---------------------------------------------------------------------------
# save_error_log
# ---------------------------------------------------------------------------


class TestSaveErrorLog:
    def test_save_writes_json(
        self,
        monitor: RobotErrorMonitor,
        mock_dashboard: MagicMock,
        tmp_path: pytest.TempPathFactory,
    ) -> None:
        import json

        mock_dashboard.get_error_id.return_value = (1001,)
        filepath = str(tmp_path / "errors.json")  # type: ignore[operator]
        monitor.save_error_log(filename=filepath, language="en")
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        assert "errMsg" in data
        assert len(data["errMsg"]) == 1

    def test_save_does_not_raise_when_no_errors(
        self,
        monitor: RobotErrorMonitor,
        mock_dashboard: MagicMock,
        tmp_path: pytest.TempPathFactory,
    ) -> None:
        mock_dashboard.get_error_id.return_value = ()
        filepath = str(tmp_path / "empty.json")  # type: ignore[operator]
        monitor.save_error_log(filename=filepath, language="en")
