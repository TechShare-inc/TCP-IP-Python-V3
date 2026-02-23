"""HIL (hardware-in-the-loop) tests — require a real Dobot robot.

All tests in this module are automatically skipped unless the environment
variable ``DOBOT_TEST_IP`` points to a reachable robot.

Run with::

    DOBOT_TEST_IP=192.168.1.6 pytest tests/hil -v -m hil

See tests/hil/conftest.py for connection configuration.
"""

from __future__ import annotations

import pytest

from dobot_api_v3.dashboard import DobotApiDashboard
from dobot_api_v3.feedback import DobotApiFeedback
from dobot_api_v3.move import DobotApiMove
from dobot_api_v3.robot import DobotRobot
from tests.hil.conftest import requires_hardware

pytestmark = [pytest.mark.hil, requires_hardware]


# ---------------------------------------------------------------------------
# Dashboard — basic state queries
# ---------------------------------------------------------------------------


class TestDashboardHIL:
    def test_enable_disable_cycle(self, real_dashboard: DobotApiDashboard) -> None:
        """Enable the robot, read its mode, then disable it."""
        result = real_dashboard.enable_robot()
        assert "0" in result, f"enable_robot() returned: {result!r}"

        mode = real_dashboard.robot_mode()
        assert isinstance(mode, str)

        result = real_dashboard.disable_robot()
        assert "0" in result, f"disable_robot() returned: {result!r}"

    def test_get_angle_returns_string(self, real_dashboard: DobotApiDashboard) -> None:
        response = real_dashboard.get_angle()
        assert isinstance(response, str)
        assert len(response) > 0

    def test_get_pose_returns_string(self, real_dashboard: DobotApiDashboard) -> None:
        response = real_dashboard.get_pose()
        assert isinstance(response, str)
        assert len(response) > 0

    def test_get_error_id_returns_string(
        self, real_dashboard: DobotApiDashboard
    ) -> None:
        response = real_dashboard.get_error_id()
        assert isinstance(response, str)

    def test_speed_factor_accepted(self, real_dashboard: DobotApiDashboard) -> None:
        response = real_dashboard.speed_factor(50)
        assert "0" in response


# ---------------------------------------------------------------------------
# Feedback — binary packet stream
# ---------------------------------------------------------------------------


class TestFeedbackHIL:
    def test_reads_10_valid_feedback_packets(
        self, real_feedback: DobotApiFeedback
    ) -> None:
        """Read 10 consecutive packets and verify they are non-None numpy arrays."""
        import numpy as np
        from dobot_api_v3.base import FeedbackDtype

        for i in range(10):
            packet = real_feedback.feedback_data()
            assert packet is not None, f"Packet {i} was None"
            assert packet.dtype == FeedbackDtype
            assert packet.shape == (1,)

    def test_robot_mode_field_is_plausible(
        self, real_feedback: DobotApiFeedback
    ) -> None:
        """robot_mode should be a non-negative integer."""
        packet = real_feedback.feedback_data()
        assert packet is not None
        mode = int(packet[0]["robot_mode"])
        assert mode >= 0, f"Unexpected robot_mode: {mode}"


# ---------------------------------------------------------------------------
# Error monitor
# ---------------------------------------------------------------------------


class TestErrorMonitorHIL:
    def test_get_error_id_format(self, real_dashboard: DobotApiDashboard) -> None:
        """GetErrorID() response must be parseable (contains digits)."""
        import re

        response = real_dashboard.get_error_id()
        codes = re.findall(r"-?\d+", response)
        assert len(codes) > 0, f"No numeric codes in response: {response!r}"


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
        response = real_dashboard.robot_mode()
        assert isinstance(response, str)


# ---------------------------------------------------------------------------
# DobotRobot — unified wrapper on real hardware
# ---------------------------------------------------------------------------


class TestDobotRobotHIL:
    """Hardware tests for the DobotRobot high-level wrapper."""

    def test_startup_and_shutdown(self, real_robot: DobotRobot) -> None:
        """Full startup/shutdown cycle must complete without errors."""
        real_robot.startup(speed=30)
        mode = real_robot.robot_mode()
        assert isinstance(mode, str)
        real_robot.shutdown()

    def test_check_errors_returns_bool(self, real_robot: DobotRobot) -> None:
        """check_errors() must return a boolean on real hardware."""
        result = real_robot.check_errors(language="en")
        assert isinstance(result, bool)

    def test_get_pose_returns_string(self, real_robot: DobotRobot) -> None:
        response = real_robot.get_pose()
        assert isinstance(response, str)
        assert len(response) > 0

    def test_get_angle_returns_string(self, real_robot: DobotRobot) -> None:
        response = real_robot.get_angle()
        assert isinstance(response, str)
        assert len(response) > 0

    def test_speed_factor_accepted(self, real_robot: DobotRobot) -> None:
        response = real_robot.speed_factor(40)
        assert "0" in response

    def test_feedback_data_returns_valid_packet(self, real_robot: DobotRobot) -> None:
        """feedback_data() should lazily connect and return a FeedbackData."""
        from dobot_api_v3.base import FeedbackData

        data = real_robot.feedback_data()
        assert data is not None
        assert isinstance(data, FeedbackData)

    def test_raw_feedback_data_returns_numpy(self, real_robot: DobotRobot) -> None:
        """raw_feedback_data() should return a structured NumPy array."""
        import numpy as np
        from dobot_api_v3.base import FeedbackDtype

        raw = real_robot.raw_feedback_data()
        assert raw is not None
        assert raw.dtype == FeedbackDtype
        assert raw.shape == (1,)

    def test_reconnect_restores_communication(self, real_robot: DobotRobot) -> None:
        """After reconnect(), forwarded commands must still work."""
        real_robot.reconnect()
        response = real_robot.robot_mode()
        assert isinstance(response, str)
