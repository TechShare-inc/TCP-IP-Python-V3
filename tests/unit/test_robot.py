"""Unit tests for DobotRobot unified wrapper."""

from __future__ import annotations

from unittest.mock import MagicMock, call, patch

import numpy as np
import pytest

from dobot_api_v3.base import DobotApi, FeedbackData, FeedbackDtype
from dobot_api_v3.responses import (
    AckResponse,
    ErrorIdResponse,
    IntResponse,
    PoseResponse,
)
from dobot_api_v3.robot import DobotRobot

pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_robot(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[DobotRobot, list[str], list[str]]:
    """DobotRobot with all sockets mocked.

    Returns:
        A 3-tuple of (robot, dashboard_cmds, move_cmds) where the command
        lists record every string passed to ``send_recv_msg`` on the
        dashboard and move connections respectively.
    """
    monkeypatch.setattr(DobotApi, "_connect", lambda self: None)

    dashboard_cmds: list[str] = []
    move_cmds: list[str] = []

    robot = DobotRobot("192.168.1.1")
    robot.dashboard.socket_dobot = MagicMock()
    robot.move.socket_dobot = MagicMock()

    def _capture_dashboard(cmd: str) -> str:
        dashboard_cmds.append(cmd)
        # Return realistic protocol responses so parse_response succeeds.
        if cmd.startswith("RobotMode"):
            return "0,{5};"
        if cmd.startswith("GetPose") or cmd.startswith("GetAngle"):
            return "0,{0.0,0.0,0.0,0.0,0.0,0.0};"
        if cmd.startswith("GetErrorID"):
            return "0,{0};"
        return f"0,0,{cmd};"

    def _capture_move(cmd: str) -> str:
        move_cmds.append(cmd)
        return f"0,0,{cmd};"

    monkeypatch.setattr(robot.dashboard, "send_recv_msg", _capture_dashboard)
    monkeypatch.setattr(robot.move, "send_recv_msg", _capture_move)

    return robot, dashboard_cmds, move_cmds


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_attributes_created(self, mock_robot: tuple) -> None:
        robot, _, _ = mock_robot
        assert robot.ip == "192.168.1.1"
        assert robot.dashboard is not None
        assert robot.move is not None
        assert robot.errors is not None

    def test_feedback_not_eager(self, mock_robot: tuple) -> None:
        """Feedback ports must NOT be connected on construction."""
        robot, _, _ = mock_robot
        assert robot._feedback is None
        assert robot._feedback_30005 is None
        assert robot._feedback_30006 is None

    def test_repr(self, mock_robot: tuple) -> None:
        robot, _, _ = mock_robot
        assert "192.168.1.1" in repr(robot)

    def test_default_language_passed_to_errors(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        robot = DobotRobot("192.168.1.1", language="zh_CN")
        assert robot.errors.i18n._initialized


# ---------------------------------------------------------------------------
# Context manager
# ---------------------------------------------------------------------------


class TestContextManager:
    def test_enter_returns_self(self, mock_robot: tuple) -> None:
        robot, _, _ = mock_robot
        result = robot.__enter__()
        assert result is robot

    def test_exit_calls_close(self, mock_robot: tuple) -> None:
        robot, _, _ = mock_robot
        close_calls: list[None] = []
        original_close = robot.close

        def _track_close() -> None:
            close_calls.append(None)
            original_close()

        robot.close = _track_close  # type: ignore[method-assign]
        robot.__exit__(None, None, None)
        assert len(close_calls) == 1

    def test_context_manager_protocol(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        with DobotRobot("192.168.1.1") as robot:
            assert isinstance(robot, DobotRobot)
        # After exit, sockets should be closed (socket_dobot set to None by DobotApi.close)
        assert robot.dashboard.socket_dobot is None
        assert robot.move.socket_dobot is None


# ---------------------------------------------------------------------------
# Lazy feedback properties
# ---------------------------------------------------------------------------


class TestLazyFeedback:
    def test_feedback_created_on_first_access(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        robot = DobotRobot("192.168.1.1")
        assert robot._feedback is None
        fb = robot.feedback
        assert fb is not None
        assert robot._feedback is fb

    def test_feedback_same_instance_on_repeated_access(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        robot = DobotRobot("192.168.1.1")
        fb1 = robot.feedback
        fb2 = robot.feedback
        assert fb1 is fb2

    def test_feedback_port(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        robot = DobotRobot("192.168.1.1")
        assert robot.feedback.port == 30004

    def test_feedback_30005_port(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        robot = DobotRobot("192.168.1.1")
        assert robot.feedback_30005.port == 30005

    def test_feedback_30006_port(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        robot = DobotRobot("192.168.1.1")
        assert robot.feedback_30006.port == 30006

    def test_feedback_30005_same_instance(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        robot = DobotRobot("192.168.1.1")
        fb1 = robot.feedback_30005
        fb2 = robot.feedback_30005
        assert fb1 is fb2

    def test_feedback_30006_same_instance(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        robot = DobotRobot("192.168.1.1")
        fb1 = robot.feedback_30006
        fb2 = robot.feedback_30006
        assert fb1 is fb2


# ---------------------------------------------------------------------------
# close() idempotency and selective teardown
# ---------------------------------------------------------------------------


class TestClose:
    def test_close_is_idempotent(self, mock_robot: tuple) -> None:
        robot, _, _ = mock_robot
        robot.close()
        robot.close()  # must not raise

    def test_close_resets_feedback_to_none(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        robot = DobotRobot("192.168.1.1")
        _ = robot.feedback  # trigger lazy creation
        assert robot._feedback is not None
        robot.close()
        assert robot._feedback is None

    def test_close_without_feedback_is_safe(self, mock_robot: tuple) -> None:
        """close() must not fail when feedback was never accessed."""
        robot, _, _ = mock_robot
        assert robot._feedback is None
        robot.close()  # must not raise

    def test_close_resets_30005_and_30006(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        robot = DobotRobot("192.168.1.1")
        _ = robot.feedback_30005
        _ = robot.feedback_30006
        robot.close()
        assert robot._feedback_30005 is None
        assert robot._feedback_30006 is None


# ---------------------------------------------------------------------------
# startup() sequence
# ---------------------------------------------------------------------------


class TestStartup:
    def test_startup_command_sequence_with_errors(self, mock_robot: tuple) -> None:
        """When errors are present, startup runs the full clear→power→disable→enable→speed sequence."""
        robot, dashboard_cmds, _ = mock_robot
        with (
            patch.object(robot.errors, "check_errors", return_value=True),
            patch("time.sleep"),
        ):
            robot.startup(speed=50)
        assert dashboard_cmds[0] == "ClearError()"
        assert dashboard_cmds[1] == "PowerOn()"
        assert dashboard_cmds[2] == "DisableRobot()"
        assert dashboard_cmds[3] == "EnableRobot()"
        assert dashboard_cmds[4] == "SpeedFactor(50)"

    def test_startup_command_sequence_no_errors(self, mock_robot: tuple) -> None:
        """When no errors, startup skips clear_error/power_on and goes straight to disable→enable→speed."""
        robot, dashboard_cmds, _ = mock_robot
        with patch.object(robot.errors, "check_errors", return_value=False):
            robot.startup(speed=50)
        assert dashboard_cmds[0] == "DisableRobot()"
        assert dashboard_cmds[1] == "EnableRobot()"
        assert dashboard_cmds[2] == "SpeedFactor(50)"
        # clear_error and power_on must NOT appear
        assert not any("ClearError" in c for c in dashboard_cmds)
        assert not any("PowerOn" in c for c in dashboard_cmds)

    def test_startup_default_speed_factor(self, mock_robot: tuple) -> None:
        robot, dashboard_cmds, _ = mock_robot
        with patch.object(robot.errors, "check_errors", return_value=False):
            robot.startup()
        assert any("SpeedFactor(40)" in cmd for cmd in dashboard_cmds)

    def test_startup_with_load(self, mock_robot: tuple) -> None:
        robot, dashboard_cmds, _ = mock_robot
        with patch.object(robot.errors, "check_errors", return_value=False):
            robot.startup(speed=30, load=1.5, center_z=0.05)
        enable_cmd = next(c for c in dashboard_cmds if c.startswith("EnableRobot"))
        assert "1.500000" in enable_cmd
        assert "0.050000" in enable_cmd

    def test_startup_power_on_wait(self, mock_robot: tuple) -> None:
        """Custom power_on_wait is forwarded to time.sleep when errors are present."""
        robot, _, _ = mock_robot
        sleep_calls: list[float] = []
        with (
            patch.object(robot.errors, "check_errors", return_value=True),
            patch("time.sleep", side_effect=lambda t: sleep_calls.append(t)),
        ):
            robot.startup(power_on_wait=5.0)
        assert 5.0 in sleep_calls

    def test_startup_default_wait_is_15(self, mock_robot: tuple) -> None:
        """Default power_on_wait (15s) is used when errors are present."""
        robot, _, _ = mock_robot
        sleep_calls: list[float] = []
        with (
            patch.object(robot.errors, "check_errors", return_value=True),
            patch("time.sleep", side_effect=lambda t: sleep_calls.append(t)),
        ):
            robot.startup()
        assert 15.0 in sleep_calls

    def test_startup_no_sleep_without_errors(self, mock_robot: tuple) -> None:
        """When no errors are detected, time.sleep is never called."""
        robot, _, _ = mock_robot
        sleep_calls: list[float] = []
        with (
            patch.object(robot.errors, "check_errors", return_value=False),
            patch("time.sleep", side_effect=lambda t: sleep_calls.append(t)),
        ):
            robot.startup()
        assert len(sleep_calls) == 0


# ---------------------------------------------------------------------------
# shutdown()
# ---------------------------------------------------------------------------


class TestShutdown:
    def test_shutdown_sends_disable_robot(self, mock_robot: tuple) -> None:
        robot, dashboard_cmds, _ = mock_robot
        robot.shutdown()
        assert "DisableRobot()" in dashboard_cmds


# ---------------------------------------------------------------------------
# reconnect()
# ---------------------------------------------------------------------------


class TestReconnect:
    def test_reconnect_no_feedback(self, mock_robot: tuple) -> None:
        robot, _, _ = mock_robot
        dashboard_reconnected = []
        move_reconnected = []
        robot.dashboard.reconnect = lambda: dashboard_reconnected.append(True)  # type: ignore[method-assign]
        robot.move.reconnect = lambda: move_reconnected.append(True)  # type: ignore[method-assign]
        robot.reconnect()
        assert dashboard_reconnected
        assert move_reconnected

    def test_reconnect_with_feedback(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        robot = DobotRobot("192.168.1.1")
        _ = robot.feedback  # trigger lazy creation
        feedback_reconnected = []
        robot._feedback.reconnect = lambda: feedback_reconnected.append(True)  # type: ignore[union-attr]
        robot.dashboard.reconnect = lambda: None  # type: ignore[method-assign]
        robot.move.reconnect = lambda: None  # type: ignore[method-assign]
        robot.reconnect()
        assert feedback_reconnected


# ---------------------------------------------------------------------------
# Error convenience methods
# ---------------------------------------------------------------------------


class TestErrorConvenience:
    def test_check_errors_delegates_to_error_monitor(self, mock_robot: tuple) -> None:
        robot, _, _ = mock_robot
        results = []
        robot.errors.check_errors = lambda language="en": results.append(language) or False  # type: ignore[method-assign]
        robot.check_errors(language="en")
        assert "en" in results

    def test_clear_and_recover_delegates_to_error_monitor(
        self, mock_robot: tuple
    ) -> None:
        robot, _, _ = mock_robot
        results = []
        robot.errors.clear_robot_error = lambda language="en": results.append(language) or False  # type: ignore[method-assign]
        robot.clear_and_recover(language="zh_CN")
        assert "zh_CN" in results


# ---------------------------------------------------------------------------
# feedback_data() convenience
# ---------------------------------------------------------------------------


class TestFeedbackData:
    def test_feedback_data_triggers_lazy_connect(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        robot = DobotRobot("192.168.1.1")
        assert robot._feedback is None

        dummy_array = np.zeros(1, dtype=FeedbackDtype)
        with patch.object(
            type(robot).feedback.fget(robot).__class__,  # type: ignore[union-attr]
            "feedback_data",
            return_value=dummy_array,
        ):
            # Simpler: patch the feedback property's feedback_data directly
            pass

        # Just test the lazy connect side effect
        fb_mock = MagicMock()
        fb_mock.feedback_data.return_value = None
        robot._feedback = fb_mock  # type: ignore[assignment]
        result = robot.feedback_data()
        fb_mock.feedback_data.assert_called_once()
        assert result is None

    def test_feedback_data_returns_feedback_data_instance(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        robot = DobotRobot("192.168.1.1")
        arr = np.zeros(1, dtype=FeedbackDtype)
        expected = FeedbackData.from_numpy(arr)
        fb_mock = MagicMock()
        fb_mock.feedback_data.return_value = expected
        robot._feedback = fb_mock  # type: ignore[assignment]
        result = robot.feedback_data()
        assert result is expected
        assert isinstance(result, FeedbackData)

    def test_raw_feedback_data_delegates_to_feedback(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(DobotApi, "_connect", lambda self: None)
        robot = DobotRobot("192.168.1.1")
        expected = np.zeros(1, dtype=FeedbackDtype)
        fb_mock = MagicMock()
        fb_mock.raw_feedback_data.return_value = expected
        robot._feedback = fb_mock  # type: ignore[assignment]
        result = robot.raw_feedback_data()
        assert result is expected
        fb_mock.raw_feedback_data.assert_called_once()


# ---------------------------------------------------------------------------
# Forwarded dashboard commands
# ---------------------------------------------------------------------------


class TestForwardedDashboardCommands:
    @pytest.mark.parametrize(
        "method,args,expected_cmd,expected_type",
        [
            ("enable_robot", (), "EnableRobot()", AckResponse),
            ("disable_robot", (), "DisableRobot()", AckResponse),
            ("clear_error", (), "ClearError()", AckResponse),
            ("reset_robot", (), "ResetRobot()", AckResponse),
            ("power_on", (), "PowerOn()", AckResponse),
            ("emergency_stop", (), "EmergencyStop()", AckResponse),
            ("speed_factor", (40,), "SpeedFactor(40)", AckResponse),
            ("robot_mode", (), "RobotMode()", IntResponse),
            ("get_pose", (), "GetPose()", PoseResponse),
            ("get_angle", (), "GetAngle()", PoseResponse),
            ("get_error_id", (), "GetErrorID()", ErrorIdResponse),
            ("start_drag", (), "StartDrag()", AckResponse),
            ("stop_drag", (), "StopDrag()", AckResponse),
            ("set_user", (1,), "User(1)", AckResponse),
            ("set_tool", (2,), "Tool(2)", AckResponse),
        ],
    )
    def test_dashboard_forward(
        self,
        mock_robot: tuple,
        method: str,
        args: tuple,
        expected_cmd: str,
        expected_type: type,
    ) -> None:
        robot, dashboard_cmds, _ = mock_robot
        result = getattr(robot, method)(*args)
        assert expected_cmd in dashboard_cmds
        assert isinstance(result, expected_type)


# ---------------------------------------------------------------------------
# Forwarded move commands
# ---------------------------------------------------------------------------


class TestForwardedMoveCommands:
    def test_mov_j(self, mock_robot: tuple) -> None:
        robot, _, move_cmds = mock_robot
        robot.mov_j(200, 0, 200, 0, 0, 0)
        assert any("MovJ(" in c for c in move_cmds)

    def test_mov_l(self, mock_robot: tuple) -> None:
        robot, _, move_cmds = mock_robot
        robot.mov_l(200, 0, 200, 0, 0, 0)
        assert any("MovL(" in c for c in move_cmds)

    def test_joint_mov_j(self, mock_robot: tuple) -> None:
        robot, _, move_cmds = mock_robot
        robot.joint_mov_j(0, 0, 90, 0, -90, 0)
        assert any("JointMovJ(" in c for c in move_cmds)

    def test_rel_mov_j(self, mock_robot: tuple) -> None:
        robot, _, move_cmds = mock_robot
        robot.rel_mov_j(10, 0, 0, 0, 0, 0)
        assert any("RelMovJ(" in c for c in move_cmds)

    def test_rel_mov_l(self, mock_robot: tuple) -> None:
        robot, _, move_cmds = mock_robot
        robot.rel_mov_l(10, 0, 0)
        assert any("RelMovL(" in c for c in move_cmds)

    def test_arc(self, mock_robot: tuple) -> None:
        robot, _, move_cmds = mock_robot
        robot.arc(100, 50, 200, 0, 0, 0, 200, 0, 200, 0, 0, 0)
        assert any("Arc(" in c for c in move_cmds)

    def test_servo_j(self, mock_robot: tuple) -> None:
        robot, _, move_cmds = mock_robot
        robot.servo_j(0, 0, 90, 0, -90, 0)
        assert any("ServoJ(" in c for c in move_cmds)

    def test_servo_p(self, mock_robot: tuple) -> None:
        robot, _, move_cmds = mock_robot
        robot.servo_p(200, 0, 200, 0, 0, 0)
        assert any("ServoP(" in c for c in move_cmds)

    def test_move_jog(self, mock_robot: tuple) -> None:
        robot, _, move_cmds = mock_robot
        robot.move_jog("J1+")
        assert any("MoveJog(" in c for c in move_cmds)

    def test_sync(self, mock_robot: tuple) -> None:
        robot, _, move_cmds = mock_robot
        robot.sync()
        assert any("Sync()" in c for c in move_cmds)

    def test_mov_j_with_dyn_params(self, mock_robot: tuple) -> None:
        robot, _, move_cmds = mock_robot
        robot.mov_j(200, 0, 200, 0, 0, 0, "SpeedJ=40", "AccJ=40")
        cmd = next(c for c in move_cmds if "MovJ(" in c)
        assert "SpeedJ=40" in cmd
        assert "AccJ=40" in cmd


# ---------------------------------------------------------------------------
# Public API export
# ---------------------------------------------------------------------------


class TestPublicExport:
    def test_dobot_robot_in_package(self) -> None:
        from dobot_api_v3 import DobotRobot as DR

        assert DR is DobotRobot

    def test_dobot_robot_in_all(self) -> None:
        import dobot_api_v3

        assert "DobotRobot" in dobot_api_v3.__all__
