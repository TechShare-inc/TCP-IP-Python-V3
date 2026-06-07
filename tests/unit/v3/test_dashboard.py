"""Unit tests for V3 DobotApiDashboard command serialization.

Verifies that V3 dashboard methods generate the correct wire-format
command strings and parse responses correctly.  Uses a mock socket
to avoid requiring a real robot.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from dobot_api.v3 import DobotApiDashboard


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def dashboard() -> DobotApiDashboard:
    """Create a dashboard with a mocked send_recv_msg."""
    with patch("dobot_api_v3.base.DobotApi._connect", return_value=None):
        with patch("dobot_api_v3.base.DobotApi.close", return_value=None):
            dash = DobotApiDashboard.__new__(DobotApiDashboard)
            dash.ip = "192.168.1.6"
            dash.port = 29999
            dash.socket_dobot = MagicMock()
            dash._global_lock = MagicMock()
            dash._raw_send_recv = MagicMock()
            # Wire up send_recv_msg through the MRO
            return dash


def _patch_send_recv(dash: DobotApiDashboard, response: str) -> MagicMock:
    """Patch the dashboard's send_recv_msg to return a canned response."""
    mock = MagicMock(return_value=response)
    # We need to patch on the actual DobotApi instance in the MRO
    with patch.object(
        dash, "send_recv_msg", mock, create=True
    ):
        yield mock


# ---------------------------------------------------------------------------
# System / lifecycle commands
# ---------------------------------------------------------------------------


class TestSystemCommands:
    def test_enable_robot_sends_correct_string(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},EnableRobot(0.000000,0.000000,0.000000,0.000000);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.enable_robot()
        sent = mock.call_args[0][0]
        assert sent.startswith("EnableRobot(")

    def test_disable_robot_sends_correct_string(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},DisableRobot();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.disable_robot()
        assert mock.call_args[0][0] == "DisableRobot()"

    def test_clear_error_sends_correct_string(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},ClearError();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.clear_error()
        assert mock.call_args[0][0] == "ClearError()"

    def test_reset_robot_sends_correct_string(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},ResetRobot();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.reset_robot()
        assert mock.call_args[0][0] == "ResetRobot()"

    def test_power_on_sends_correct_string(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},PowerOn();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.power_on()
        assert mock.call_args[0][0] == "PowerOn()"

    def test_emergency_stop_sends_correct_string(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},EmergencyStop();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.emergency_stop()
        assert mock.call_args[0][0] == "EmergencyStop()"

    def test_speed_factor_sends_correct_string(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},SpeedFactor(50);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.speed_factor(50)
        assert "SpeedFactor(50)" in mock.call_args[0][0]

    def test_robot_mode_parses_int(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{5},RobotMode();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.robot_mode()
        assert result == 5

    def test_pause_sends_correct_string(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},pause();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.pause()
        assert mock.call_args[0][0] == "pause()"

    def test_resume_sends_continue_string(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},continue();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.resume()
        assert mock.call_args[0][0] == "continue()"


# ---------------------------------------------------------------------------
# Config commands
# ---------------------------------------------------------------------------


class TestConfigCommands:
    def test_acc_j_sends_correct_string(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},AccJ(100);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.acc_j(100)
        assert "AccJ(100)" in mock.call_args[0][0]

    def test_acc_l_sends_correct_string(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},AccL(100);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.acc_l(100)
        assert "AccL(100)" in mock.call_args[0][0]

    def test_speed_j_sends_correct_string(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},SpeedJ(30);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.speed_j(30)
        assert "SpeedJ(30)" in mock.call_args[0][0]

    def test_speed_l_sends_correct_string(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},SpeedL(30);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.speed_l(30)
        assert "SpeedL(30)" in mock.call_args[0][0]

    def test_arch_sends_correct_string(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},Arch(1);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.arch(1)
        assert "Arch(1)" in mock.call_args[0][0]

    def test_set_arm_orientation_sends_correct_string(
        self, dashboard: DobotApiDashboard
    ) -> None:
        mock = MagicMock(return_value="0,{0},SetArmOrientation(1,0,0,1);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.set_arm_orientation(1, 0, 0, 1)
        assert "SetArmOrientation(1,0,0,1)" in mock.call_args[0][0]


# ---------------------------------------------------------------------------
# Query commands
# ---------------------------------------------------------------------------


class TestQueryCommands:
    def test_get_pose_parses_pose(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(
            return_value="0,{200.0,0.0,300.0,180.0,0.0,90.0},GetPose();"
        )
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.get_pose()
        assert result == pytest.approx((200.0, 0.0, 300.0, 180.0, 0.0, 90.0))

    def test_get_angle_parses_pose(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(
            return_value="0,{10.0,20.0,30.0,40.0,50.0,60.0},GetAngle();"
        )
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.get_angle()
        assert len(result) == 6

    def test_get_error_id_parses_tuple(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0,16,0,0,0,0,0,0},GetErrorID();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.get_error_id()
        assert 16 in result


# ---------------------------------------------------------------------------
# I/O commands
# ---------------------------------------------------------------------------


class TestIOCommands:
    def test_di_returns_int(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{1},DI(0);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.di(0)
        assert result == 1

    def test_do_output_sends_correct_string(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},DO(1,1);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            dashboard.do_output(1, 1)
        assert "DO(1,1)" in mock.call_args[0][0]
