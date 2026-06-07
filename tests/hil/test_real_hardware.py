"""HIL (hardware-in-the-loop) tests -- require a real Dobot robot.

All tests in this module are automatically skipped unless the environment
variable ``DOBOT_TEST_IP`` points to a reachable robot.

Run with::

    DOBOT_TEST_IP=192.168.1.6 pytest tests/hil -v -m hil

See tests/hil/conftest.py for connection configuration.

Return type expectations
------------------------
Dashboard/move methods now return **parsed Python types** (``int``,
``tuple[float, ...]``, ``tuple[int, ...]``) rather than raw response strings.
All assertions in this module use the parsed types.
"""

from __future__ import annotations

import pytest

from dobot_api import DobotRobot
from dobot_api import FeedbackData as UnifiedFeedbackData
from dobot_api.v3 import (
    DobotApiDashboard,
    DobotApiFeedback,
    FeedbackData,
    FeedbackDtype,
)
from tests.hil.conftest import requires_hardware

pytestmark = [pytest.mark.hil, requires_hardware]


# ---------------------------------------------------------------------------
# Dashboard -- basic state queries (all return parsed types)
# ---------------------------------------------------------------------------


class TestDashboardHIL:
    def test_enable_disable_cycle(self, real_dashboard: DobotApiDashboard) -> None:
        """Enable the robot, read its mode, then disable it."""
        cmd_id = real_dashboard.enable_robot()
        assert isinstance(cmd_id, int)

        mode = real_dashboard.robot_mode()
        assert isinstance(mode, int)
        assert mode >= 0

        cmd_id = real_dashboard.disable_robot()
        assert isinstance(cmd_id, int)

    def test_get_angle_returns_pose_tuple(
        self, real_dashboard: DobotApiDashboard
    ) -> None:
        response = real_dashboard.get_angle()
        assert isinstance(response, tuple)
        assert len(response) == 6
        assert all(isinstance(v, float) for v in response)

    def test_get_pose_returns_pose_tuple(
        self, real_dashboard: DobotApiDashboard
    ) -> None:
        response = real_dashboard.get_pose()
        assert isinstance(response, tuple)
        assert len(response) == 6
        assert all(isinstance(v, float) for v in response)

    def test_get_error_id_returns_tuple(
        self, real_dashboard: DobotApiDashboard
    ) -> None:
        result = real_dashboard.get_error_id()
        assert isinstance(result, tuple)
        assert all(isinstance(v, int) for v in result)

    def test_speed_factor_accepted(self, real_dashboard: DobotApiDashboard) -> None:
        cmd_id = real_dashboard.speed_factor(50)
        assert isinstance(cmd_id, int)


# ---------------------------------------------------------------------------
# Feedback -- binary packet stream
# ---------------------------------------------------------------------------


class TestFeedbackHIL:
    def test_reads_10_valid_feedback_data(
        self, real_feedback: DobotApiFeedback
    ) -> None:
        """Read 10 consecutive packets as typed FeedbackData instances."""
        for i in range(10):
            data = real_feedback.feedback_data()
            assert data is not None, f"Packet {i} was None"
            assert isinstance(data, FeedbackData)

    def test_raw_feedback_returns_numpy(self, real_feedback: DobotApiFeedback) -> None:
        """raw_feedback_data() must return a structured NumPy array."""

        raw = real_feedback.raw_feedback_data()
        assert raw is not None
        assert raw.dtype == FeedbackDtype
        assert raw.shape == (1,)

    def test_robot_mode_field_is_plausible(
        self, real_feedback: DobotApiFeedback
    ) -> None:
        """robot_mode should be a non-negative integer."""
        data = real_feedback.feedback_data()
        assert data is not None
        assert isinstance(data.robot_mode, int)
        assert data.robot_mode >= 0


# ---------------------------------------------------------------------------
# Error monitor
# ---------------------------------------------------------------------------


class TestErrorMonitorHIL:
    def test_get_error_id_returns_int_tuple(
        self, real_dashboard: DobotApiDashboard
    ) -> None:
        """get_error_id() must return a tuple of ints."""
        result = real_dashboard.get_error_id()
        assert isinstance(result, tuple)
        assert all(isinstance(v, int) for v in result)


# ---------------------------------------------------------------------------
# Reconnect after manual socket close (simulates controller restart)
# ---------------------------------------------------------------------------


class TestReconnectHIL:
    def test_reconnect_restores_communication(
        self, real_dashboard: DobotApiDashboard
    ) -> None:
        """After closing the socket and calling reconnect(), the API should work again."""
        real_dashboard.socket_dobot.close()  # type: ignore[union-attr]
        real_dashboard.socket_dobot = None
        real_dashboard.reconnect()
        mode = real_dashboard.robot_mode()
        assert isinstance(mode, int)


# ---------------------------------------------------------------------------
# DobotRobot -- unified wrapper on real hardware
# ---------------------------------------------------------------------------


class TestDobotRobotHIL:
    """Hardware tests for the DobotRobot high-level wrapper."""

    def test_startup_and_shutdown(self, real_robot: DobotRobot) -> None:
        """Full startup/shutdown cycle must complete without errors."""
        real_robot.startup(speed=30)
        mode = real_robot.robot_mode()
        assert isinstance(mode, int)
        real_robot.shutdown()

    def test_check_errors_returns_bool(self, real_robot: DobotRobot) -> None:
        """check_errors() must return a boolean on real hardware."""
        result = real_robot.check_errors(language="en")
        assert isinstance(result, bool)

    def test_get_pose_returns_pose_tuple(self, real_robot: DobotRobot) -> None:
        response = real_robot.get_pose()
        assert isinstance(response, tuple)
        assert len(response) == 6
        assert all(isinstance(v, float) for v in response)

    def test_get_angle_returns_pose_tuple(self, real_robot: DobotRobot) -> None:
        response = real_robot.get_angle()
        assert isinstance(response, tuple)
        assert len(response) == 6
        assert all(isinstance(v, float) for v in response)

    def test_speed_factor_accepted(self, real_robot: DobotRobot) -> None:
        cmd_id = real_robot.speed_factor(40)
        assert isinstance(cmd_id, int)

    def test_feedback_data_returns_valid_packet(self, real_robot: DobotRobot) -> None:
        """feedback_data() should lazily connect and return a FeedbackData."""
        data = real_robot.feedback_data()
        assert data is not None
        assert isinstance(data, UnifiedFeedbackData)

    def test_raw_feedback_data_returns_numpy(self, real_robot: DobotRobot) -> None:
        """raw_feedback_data() should return a structured NumPy array."""

        raw = real_robot.raw_feedback_data()
        assert raw is not None
        assert raw.dtype == FeedbackDtype
        assert raw.shape == (1,)

    def test_reconnect_restores_communication(self, real_robot: DobotRobot) -> None:
        """After reconnect(), forwarded commands must still work."""
        real_robot.reconnect()
        mode = real_robot.robot_mode()
        assert isinstance(mode, int)
