"""Unit tests for V3 DobotApiMove command serialization.

Verifies that V3 move methods generate correct wire-format command
strings and route to port 30003.  Uses a mock socket.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from dobot_api.v3 import DobotApiMove


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def move() -> DobotApiMove:
    """Create a move backend with a mocked socket."""
    with patch("dobot_api_v3.base.DobotApi._connect", return_value=None):
        with patch("dobot_api_v3.base.DobotApi.close", return_value=None):
            m = DobotApiMove.__new__(DobotApiMove)
            m.ip = "192.168.1.6"
            m.port = 30003
            m.socket_dobot = MagicMock()
            m._global_lock = MagicMock()
            return m


# ---------------------------------------------------------------------------
# Basic motion
# ---------------------------------------------------------------------------


class TestBasicMotion:
    def test_mov_j_sends_correct_format(self, move: DobotApiMove) -> None:
        mock = MagicMock(return_value="0,{0},MovJ(200.000000,0.000000,200.000000,180.000000,0.000000,90.000000);")
        with patch.object(move, "send_recv_msg", mock, create=True):
            move.mov_j(200, 0, 200, 180, 0, 90)
        sent = mock.call_args[0][0]
        assert sent.startswith("MovJ(")
        assert "200" in sent

    def test_mov_l_sends_correct_format(self, move: DobotApiMove) -> None:
        mock = MagicMock(return_value="0,{0},MovL(100.000000,0.000000,100.000000,0.000000,0.000000,0.000000);")
        with patch.object(move, "send_recv_msg", mock, create=True):
            move.mov_l(100, 0, 100, 0, 0, 0)
        sent = mock.call_args[0][0]
        assert sent.startswith("MovL(")

    def test_joint_mov_j_sends_correct_format(self, move: DobotApiMove) -> None:
        mock = MagicMock(return_value="0,{0},JointMovJ(10.000000,20.000000,30.000000,40.000000,50.000000,60.000000);")
        with patch.object(move, "send_recv_msg", mock, create=True):
            move.joint_mov_j(10, 20, 30, 40, 50, 60)
        sent = mock.call_args[0][0]
        assert sent.startswith("JointMovJ(")

    def test_arc_sends_12_position_args(self, move: DobotApiMove) -> None:
        mock = MagicMock(return_value="0,{0},Arc(1,2,3,4,5,6,7,8,9,10,11,12);")
        with patch.object(move, "send_recv_msg", mock, create=True):
            move.arc(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        sent = mock.call_args[0][0]
        assert sent.startswith("Arc(")


# ---------------------------------------------------------------------------
# Relative motion
# ---------------------------------------------------------------------------


class TestRelativeMotion:
    def test_rel_mov_j_sends_correct_format(self, move: DobotApiMove) -> None:
        mock = MagicMock(return_value="0,{0},RelMovJ(10.000000,0.000000,0.000000,0.000000,0.000000,0.000000);")
        with patch.object(move, "send_recv_msg", mock, create=True):
            move.rel_mov_j(10, 0, 0, 0, 0, 0)
        sent = mock.call_args[0][0]
        assert sent.startswith("RelMovJ(")

    def test_rel_mov_l_sends_correct_format(self, move: DobotApiMove) -> None:
        mock = MagicMock(return_value="0,{0},RelMovL(0.000000,0.000000,-50.000000);")
        with patch.object(move, "send_recv_msg", mock, create=True):
            move.rel_mov_l(0, 0, -50)
        sent = mock.call_args[0][0]
        assert sent.startswith("RelMovL(")

    def test_rel_mov_j_tool_sends_correct_format(self, move: DobotApiMove) -> None:
        mock = MagicMock(return_value="0,{0},RelMovJTool(1.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0);")
        with patch.object(move, "send_recv_msg", mock, create=True):
            move.rel_mov_j_tool(1, 0, 0, 0, 0, 0, tool=0)
        sent = mock.call_args[0][0]
        assert sent.startswith("RelMovJTool(")


# ---------------------------------------------------------------------------
# Servo / jog
# ---------------------------------------------------------------------------


class TestServoJog:
    def test_servo_j_sends_correct_format(self, move: DobotApiMove) -> None:
        mock = MagicMock(return_value="0,{0},ServoJ(1.0,2.0,3.0,4.0,5.0,6.0,0.100000,50.000000,500.000000);")
        with patch.object(move, "send_recv_msg", mock, create=True):
            move.servo_j(1, 2, 3, 4, 5, 6)
        sent = mock.call_args[0][0]
        assert sent.startswith("ServoJ(")

    def test_servo_p_sends_correct_format(self, move: DobotApiMove) -> None:
        mock = MagicMock(return_value="0,{0},ServoP(100.0,200.0,300.0,0.0,0.0,0.0);")
        with patch.object(move, "send_recv_msg", mock, create=True):
            move.servo_p(100, 200, 300, 0, 0, 0)
        sent = mock.call_args[0][0]
        assert sent.startswith("ServoP(")

    def test_move_jog_sends_axis_id(self, move: DobotApiMove) -> None:
        mock = MagicMock(return_value="0,{0},MoveJog(J1+);")
        with patch.object(move, "send_recv_msg", mock, create=True):
            move.move_jog("J1+")
        sent = mock.call_args[0][0]
        assert "MoveJog" in sent
        assert "J1+" in sent


# ---------------------------------------------------------------------------
# Trajectory
# ---------------------------------------------------------------------------


class TestTrajectory:
    def test_sync_sends_correct_string(self, move: DobotApiMove) -> None:
        mock = MagicMock(return_value="0,{0},Sync();")
        with patch.object(move, "send_recv_msg", mock, create=True):
            move.sync()
        assert mock.call_args[0][0] == "Sync()"

    def test_start_trace_sends_correct_string(self, move: DobotApiMove) -> None:
        mock = MagicMock(return_value="0,{0},StartTrace(my_trace);")
        with patch.object(move, "send_recv_msg", mock, create=True):
            move.start_trace("my_trace")
        sent = mock.call_args[0][0]
        assert sent.startswith("StartTrace(")

    def test_start_path_sends_correct_string(self, move: DobotApiMove) -> None:
        mock = MagicMock(return_value="0,{0},StartPath(my_path,0,0);")
        with patch.object(move, "send_recv_msg", mock, create=True):
            move.start_path("my_path", 0, 0)
        sent = mock.call_args[0][0]
        assert sent.startswith("StartPath(")
