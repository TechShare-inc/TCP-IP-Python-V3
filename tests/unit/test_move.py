"""Unit tests for DobotApiMove — movement command string serialization."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# Parametrized command serialization — simple forms (no dyn_params)
# ---------------------------------------------------------------------------


_MOVE_CMD_CASES = [
    # mov_j
    (
        "mov_j",
        (1.0, 2.0, 3.0, 4.0, 5.0, 6.0),
        {},
        "MovJ(1.000000,2.000000,3.000000,4.000000,5.000000,6.000000)",
    ),
    # mov_l
    (
        "mov_l",
        (10.0, 20.0, 30.0, 0.0, 0.0, 90.0),
        {},
        "MovL(10.000000,20.000000,30.000000,0.000000,0.000000,90.000000)",
    ),
    # joint_mov_j
    (
        "joint_mov_j",
        (0.0, -30.0, 60.0, 0.0, 30.0, 0.0),
        {},
        "JointMovJ(0.000000,-30.000000,60.000000,0.000000,30.000000,0.000000)",
    ),
    # rel_mov_j
    (
        "rel_mov_j",
        (5.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        {},
        "RelMovJ(5.000000,0.000000,0.000000,0.000000,0.000000,0.000000)",
    ),
    # rel_mov_l
    (
        "rel_mov_l",
        (10.0, 0.0, -5.0),
        {},
        "RelMovL(10.000000,0.000000,-5.000000)",
    ),
    # mov_l_io
    (
        "mov_l_io",
        (1.0, 2.0, 3.0, 4.0, 5.0, 6.0),
        {},
        "MovLIO(1.000000,2.000000,3.000000,4.000000,5.000000,6.000000)",
    ),
    # mov_j_io
    (
        "mov_j_io",
        (1.0, 2.0, 3.0, 4.0, 5.0, 6.0),
        {},
        "MovJIO(1.000000,2.000000,3.000000,4.000000,5.000000,6.000000)",
    ),
    # servo_js
    (
        "servo_js",
        (0.0, 0.0, 90.0, 0.0, 0.0, 0.0),
        {},
        "ServoJS(0.000000,0.000000,90.000000,0.000000,0.000000,0.000000)",
    ),
    # servo_p
    (
        "servo_p",
        (200.0, 0.0, 400.0, 0.0, 0.0, 0.0),
        {},
        "ServoP(200.000000,0.000000,400.000000,0.000000,0.000000,0.000000)",
    ),
    # sync
    ("sync", (), {}, "Sync()"),
    # rel_joint_mov_j
    (
        "rel_joint_mov_j",
        (1.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        {},
        "RelJointMovJ(1.000000,0.000000,0.000000,0.000000,0.000000,0.000000)",
    ),
    # start_trace
    (
        "start_trace",
        ("trace.traj",),
        {},
        "StartTrace(trace.traj)",
    ),
    # start_fc_trace
    (
        "start_fc_trace",
        ("fc_trace.traj",),
        {},
        "StartFCTrace(fc_trace.traj)",
    ),
    # start_path (uses f-string with spaces: "StartPath({name}, {const}, {cart})")
    (
        "start_path",
        ("path.json", 1, 0),
        {},
        "StartPath(path.json, 1, 0)",
    ),
]


@pytest.mark.parametrize("method,args,kwargs,expected", _MOVE_CMD_CASES)
def test_move_command_serialization(
    method: str,
    args: tuple,
    kwargs: dict,
    expected: str,
    mock_move: tuple,
) -> None:
    """Calling move.``method(*args)`` must send exactly ``expected`` to the robot."""
    mv, sent = mock_move
    getattr(mv, method)(*args, **kwargs)
    assert sent[-1] == expected, (
        f"{method}({args}) → got {sent[-1]!r}, want {expected!r}"
    )


# ---------------------------------------------------------------------------
# mov_j / mov_l / joint_mov_j — *dyn_params appended as str()
# ---------------------------------------------------------------------------


class TestDynParams:
    def test_mov_j_with_single_string_param(self, mock_move: tuple) -> None:
        mv, sent = mock_move
        mv.mov_j(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "SpeedJ=50")
        assert (
            sent[-1]
            == "MovJ(0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,SpeedJ=50)"
        )

    def test_mov_j_with_multiple_params(self, mock_move: tuple) -> None:
        mv, sent = mock_move
        mv.mov_j(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "SpeedJ=50", "AccJ=80")
        assert sent[-1] == (
            "MovJ(0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,SpeedJ=50,AccJ=80)"
        )

    def test_mov_l_with_tuple_param(self, mock_move: tuple) -> None:
        mv, sent = mock_move
        mv.mov_l(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, (1, 2, 0, 3))
        assert sent[-1] == (
            "MovL(0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,(1, 2, 0, 3))"
        )


# ---------------------------------------------------------------------------
# servo_j — named keyword parameters
# ---------------------------------------------------------------------------


class TestServoJ:
    def test_default_params(self, mock_move: tuple) -> None:
        mv, sent = mock_move
        mv.servo_j(0.0, 0.0, 90.0, 0.0, 0.0, 0.0)
        assert sent[-1] == (
            "ServoJ(0.000000,0.000000,90.000000,0.000000,0.000000,0.000000,"
            "t=0.100000,lookahead_time=50.000000,gain=500.000000)"
        )

    def test_custom_params(self, mock_move: tuple) -> None:
        mv, sent = mock_move
        mv.servo_j(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, t=0.5, lookahead_time=30.0, gain=300.0)
        assert sent[-1] == (
            "ServoJ(0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,"
            "t=0.500000,lookahead_time=30.000000,gain=300.000000)"
        )


# ---------------------------------------------------------------------------
# move_jog
# ---------------------------------------------------------------------------


class TestMoveJog:
    def test_axis_only(self, mock_move: tuple) -> None:
        mv, sent = mock_move
        mv.move_jog("J1+")
        assert sent[-1] == "MoveJog(J1+)"

    def test_axis_with_extra_params(self, mock_move: tuple) -> None:
        mv, sent = mock_move
        mv.move_jog("X-", "coord=1")
        assert sent[-1] == "MoveJog(X-,coord=1)"


# ---------------------------------------------------------------------------
# arc — 12-point command
# ---------------------------------------------------------------------------


class TestArc:
    def test_arc_serialization(self, mock_move: tuple) -> None:
        mv, sent = mock_move
        mv.arc(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0)
        assert sent[-1] == (
            "Arc(1.000000,2.000000,3.000000,4.000000,5.000000,6.000000,"
            "7.000000,8.000000,9.000000,10.000000,11.000000,12.000000)"
        )


# ---------------------------------------------------------------------------
# circle3
# ---------------------------------------------------------------------------


class TestCircle3:
    def test_circle3_serialization(self, mock_move: tuple) -> None:
        mv, sent = mock_move
        mv.circle3(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 3)
        assert sent[-1] == (
            "Circle3(1.000000,2.000000,3.000000,4.000000,5.000000,6.000000,"
            "7.000000,8.000000,9.000000,10.000000,11.000000,12.000000,3)"
        )


# ---------------------------------------------------------------------------
# rel_mov_j_tool / rel_mov_l_tool — ToolDynParam formatting
# ---------------------------------------------------------------------------


class TestRelMovTool:
    def test_rel_mov_j_tool_no_dyn_params(self, mock_move: tuple) -> None:
        mv, sent = mock_move
        mv.rel_mov_j_tool(1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 1)
        assert (
            sent[-1]
            == "RelMovJTool(1.000000,2.000000,3.000000,0.000000,0.000000,0.000000, 1)"
        )

    def test_rel_mov_j_tool_with_dyn_param(self, mock_move: tuple) -> None:
        mv, sent = mock_move
        mv.rel_mov_j_tool(1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 1, (100, 80, 0))
        assert sent[-1] == (
            "RelMovJTool(1.000000,2.000000,3.000000,0.000000,0.000000,0.000000, 1,"
            " SpeedJ=100, AccJ=80, User=0)"
        )

    def test_rel_mov_l_tool_with_dyn_param(self, mock_move: tuple) -> None:
        mv, sent = mock_move
        mv.rel_mov_l_tool(0.0, 0.0, 10.0, 0.0, 0.0, 0.0, 2, (50, 40, 1))
        assert sent[-1] == (
            "RelMovLTool(0.000000,0.000000,10.000000,0.000000,0.000000,0.000000, 2,"
            " SpeedJ=50, AccJ=40, User=1)"
        )


# ---------------------------------------------------------------------------
# rel_mov_j_user / rel_mov_l_user
# ---------------------------------------------------------------------------


class TestRelMovUser:
    def test_rel_mov_j_user_no_dyn_params(self, mock_move: tuple) -> None:
        mv, sent = mock_move
        mv.rel_mov_j_user(1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2)
        assert (
            sent[-1]
            == "RelMovJUser(1.000000,0.000000,0.000000,0.000000,0.000000,0.000000, 2)"
        )

    def test_rel_mov_l_user_no_dyn_params(self, mock_move: tuple) -> None:
        mv, sent = mock_move
        mv.rel_mov_l_user(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0)
        assert (
            sent[-1]
            == "RelMovLUser(0.000000,0.000000,5.000000,0.000000,0.000000,0.000000, 0)"
        )


# ---------------------------------------------------------------------------
# jump — unimplemented stub (returns None)
# ---------------------------------------------------------------------------


class TestJump:
    def test_jump_returns_none(self, mock_move: tuple) -> None:
        mv, _ = mock_move
        result = mv.jump()
        assert result is None
