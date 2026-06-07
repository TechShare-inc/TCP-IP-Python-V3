"""Unit tests for V4 DobotApiDashboard command serialization.

Verifies that V4 dashboard methods generate correct wire-format command
strings (brace-delimited payloads) and parse responses using the V4
parse_* functions.  Uses a mock socket.
"""

from __future__ import annotations

import socket as _socket
from unittest.mock import MagicMock, patch

import pytest

from dobot_api.v4 import DobotApiDashboard


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def dashboard() -> DobotApiDashboard:
    """Create a V4 dashboard with a mocked socket.

    Patches ``socket.socket`` so ``DobotApi.__init__`` does not attempt
    a real TCP connection.  The resulting object has a MagicMock socket
    that will accept any ``send`` / ``recv`` calls.
    """
    with patch("dobot_api_v4.base.socket.socket", autospec=True) as mock_sock_cls:
        mock_instance = MagicMock()
        mock_instance.getsockopt.return_value = 144000
        mock_sock_cls.return_value = mock_instance
        dash = DobotApiDashboard("192.168.1.6", 29999)
        return dash


# ---------------------------------------------------------------------------
# System / lifecycle commands
# ---------------------------------------------------------------------------


class TestSystemCommands:
    def test_enable_robot_returns_none_on_success(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0},EnableRobot(0.000000,0.000000,0.000000,0.000000);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.enable_robot()
        assert result is None

    def test_enable_robot_raises_on_error(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="-1,{some error},EnableRobot(0.000000,0.000000,0.000000,0.000000);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            with pytest.raises(Exception):
                dashboard.enable_robot()

    def test_disable_robot_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},DisableRobot();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.disable_robot()
        assert result is None

    def test_clear_error_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},ClearError();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.clear_error()
        assert result is None

    def test_power_on_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},PowerOn();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.power_on()
        assert result is None

    def test_reset_robot_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},ResetRobot();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.reset_robot()
        assert result is None

    def test_speed_factor_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},SpeedFactor(50);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.speed_factor(50)
        assert result is None

    def test_emergency_stop_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},EmergencyStop(1);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.emergency_stop(1)
        assert result is None


# ---------------------------------------------------------------------------
# Config commands
# ---------------------------------------------------------------------------


class TestConfigCommands:
    def test_acc_j_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},AccJ(100);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.acc_j(100)
        assert result is None

    def test_acc_l_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},AccL(100);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.acc_l(100)
        assert result is None

    def test_vel_j_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},VelJ(50);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.vel_j(50)
        assert result is None

    def test_vel_l_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},VelL(50);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.vel_l(50)
        assert result is None

    def test_cp_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},CP(50);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.cp(50)
        assert result is None

    def test_set_payload_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},SetPayload(1.500000,0.000000,0.000000,0.000000,F);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.set_payload(1.5)
        assert result is None

    def test_set_collision_level_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},SetCollisionLevel(3);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.set_collision_level(3)
        assert result is None


# ---------------------------------------------------------------------------
# Motion commands (V4: on dashboard, not separate port)
# ---------------------------------------------------------------------------


class TestMotionCommands:
    def test_mov_j_returns_command_id(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{42},MovJ(200.000000,0.000000,200.000000,180.000000,0.000000,90.000000,0);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.mov_j(200, 0, 200, 180, 0, 90, 0)
        assert result == 42

    def test_mov_l_returns_command_id(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{99},MovL(100.000000,0.000000,100.000000,0.000000,0.000000,0.000000,0);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.mov_l(100, 0, 100, 0, 0, 0, 0)
        assert result == 99

    def test_servo_j_returns_command_id(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{7},ServoJ(1.0,2.0,3.0,4.0,5.0,6.0,-1.000000,-1.000000,-1.000000);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.servo_j(1, 2, 3, 4, 5, 6)
        assert result == 7

    def test_servo_p_returns_command_id(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{8},ServoP(1.0,2.0,3.0,4.0,5.0,6.0,-1.000000,-1.000000,-1.000000);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.servo_p(1, 2, 3, 4, 5, 6)
        assert result == 8

    def test_move_jog_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},MoveJog(J1+);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.move_jog("J1+")
        assert result is None


# ---------------------------------------------------------------------------
# Query commands
# ---------------------------------------------------------------------------


class TestQueryCommands:
    def test_robot_mode_parses_int(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{5},RobotMode();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.robot_mode()
        assert result == 5

    def test_get_pose_parses_pose(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(
            return_value="0,{200.000000,0.000000,300.000000,180.000000,0.000000,90.000000},GetPose();"
        )
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.get_pose()
        assert result.x == 200.0
        assert result.y == 0.0
        assert result.z == 300.0

    def test_get_angle_parses_pose(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(
            return_value="0,{10.000000,20.000000,30.000000,40.000000,50.000000,60.000000},GetAngle();"
        )
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.get_angle()
        assert result.x == 10.0

    def test_get_error_id_parses_tuple(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{0,16,0,0,0,0,0,0},GetErrorID();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.get_error_id()
        assert 16 in result


# ---------------------------------------------------------------------------
# Force compliance commands (V4 only)
# ---------------------------------------------------------------------------


class TestForceCompliance:
    def test_fc_force_mode_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},FCForceMode(1,0,0,1,0,0,0,0,0,0,0,0);")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.fc_force_mode(1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        assert result is None

    def test_fc_off_returns_none(self, dashboard: DobotApiDashboard) -> None:
        mock = MagicMock(return_value="0,{},FCOff();")
        with patch.object(dashboard, "send_recv_msg", mock, create=True):
            result = dashboard.fc_off()
        assert result is None
