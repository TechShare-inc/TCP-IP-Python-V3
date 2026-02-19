"""Unit tests for DobotApiDashboard — command string serialization."""

from __future__ import annotations

import pytest

from dobot_api_v3.dashboard import DobotApiDashboard

pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# _fmt helper
# ---------------------------------------------------------------------------


class TestFmt:
    """Verify that _fmt produces the correct protocol string for each type."""

    @pytest.fixture
    def db(self, mock_dashboard: tuple) -> DobotApiDashboard:
        return mock_dashboard[0]

    @pytest.mark.parametrize(
        "value,expected",
        [
            (5, "5"),
            (0, "0"),
            (-3, "-3"),
            (1.5, "1.500000"),
            (0.0, "0.000000"),
            (-1.25, "-1.250000"),
            ("hello", "hello"),
            ("", ""),
            ([1, 2, 3], "{1,2,3}"),
            ((1, 2, 3), "{1,2,3}"),
            ([1, 1.5], "{1,1.500000}"),
            ([], "{}"),
        ],
    )
    def test_fmt_types(
        self, db: DobotApiDashboard, value: object, expected: str
    ) -> None:
        assert db._fmt(value) == expected  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# _build_cmd helper
# ---------------------------------------------------------------------------


class TestBuildCmd:
    @pytest.fixture
    def db(self, mock_dashboard: tuple) -> DobotApiDashboard:
        return mock_dashboard[0]

    def test_no_args(self, db: DobotApiDashboard) -> None:
        assert db._build_cmd("TestCmd") == "TestCmd()"

    def test_positional_int(self, db: DobotApiDashboard) -> None:
        assert db._build_cmd("DO", 1, 0) == "DO(1,0)"

    def test_positional_float(self, db: DobotApiDashboard) -> None:
        assert db._build_cmd("PayLoad", 1.5, 0.0) == "PayLoad(1.500000,0.000000)"

    def test_positional_str(self, db: DobotApiDashboard) -> None:
        assert db._build_cmd("RunScript", "myscript") == "RunScript(myscript)"

    def test_keyword_args(self, db: DobotApiDashboard) -> None:
        result = db._build_cmd("ServoJ", speed=50, acc=80)
        assert result == "ServoJ(speed=50,acc=80)"

    def test_mixed_args(self, db: DobotApiDashboard) -> None:
        result = db._build_cmd("Cmd", 1, 2.0, key="val")
        assert result == "Cmd(1,2.000000,key=val)"


# ---------------------------------------------------------------------------
# Command serialization — parametrized over all single-call methods.
# Each entry: (method_name_str, args, kwargs, expected_protocol_string)
# ---------------------------------------------------------------------------


_CMD_CASES = [
    # No-arg commands
    ("disable_robot", (), {}, "DisableRobot()"),
    ("clear_error", (), {}, "ClearError()"),
    ("reset_robot", (), {}, "ResetRobot()"),
    ("robot_mode", (), {}, "RobotMode()"),
    ("power_on", (), {}, "PowerOn()"),
    ("stop_script", (), {}, "StopScript()"),
    ("pause_script", (), {}, "PauseScript()"),
    ("continue_script", (), {}, "ContinueScript()"),
    ("get_error_id", (), {}, "GetErrorID()"),
    ("get_angle", (), {}, "GetAngle()"),
    ("get_pose", (), {}, "GetPose()"),
    ("emergency_stop", (), {}, "EmergencyStop()"),
    ("get_six_force_data", (), {}, "GetSixForceData()"),
    ("get_terminal_485", (), {}, "GetTerminal485()"),
    ("tcp_speed_end", (), {}, "TCPSpeedEnd()"),
    ("start_drag", (), {}, "StartDrag()"),
    ("stop_drag", (), {}, "StopDrag()"),
    ("pause", (), {}, "pause()"),
    ("resume", (), {}, "continue()"),
    # Single-int commands
    ("speed_factor", (75,), {}, "SpeedFactor(75)"),
    ("set_user", (2,), {}, "User(2)"),
    ("set_tool", (1,), {}, "Tool(1)"),
    ("acc_j", (80,), {}, "AccJ(80)"),
    ("acc_l", (60,), {}, "AccL(60)"),
    ("speed_j", (50,), {}, "SpeedJ(50)"),
    ("speed_l", (40,), {}, "SpeedL(40)"),
    ("arch", (3,), {}, "Arch(3)"),
    ("cp", (90,), {}, "CP(90)"),
    ("lim_z", (200,), {}, "LimZ(200)"),
    ("set_collision_level", (3,), {}, "SetCollisionLevel(3)"),
    ("set_safe_skin", (1,), {}, "SetSafeSkin(1)"),
    ("set_obstacle_avoid", (0,), {}, "SetObstacleAvoid(0)"),
    ("set_collide_drag", (1,), {}, "SetCollideDrag(1)"),
    ("set_terminal_keys", (0,), {}, "SetTerminalKeys(0)"),
    ("tcp_speed", (500,), {}, "TCPSpeed(500)"),
    ("modbus_close", (0,), {}, "ModbusClose(0)"),
    ("di", (5,), {}, "DI(5)"),
    ("tool_di", (1,), {}, "ToolDI(1)"),
    ("load_switch", (1,), {}, "LoadSwitch(1)"),
    # Two-arg commands
    ("payload", (1.5, 0.1), {}, "PayLoad(1.500000,0.100000)"),
    ("do_output", (3, 1), {}, "DO(3,1)"),
    ("do_execute", (3, 0), {}, "DOExecute(3,0)"),
    ("tool_do", (1, 1), {}, "ToolDO(1,1)"),
    ("tool_do_execute", (2, 0), {}, "ToolDOExecute(2,0)"),
    ("ao", (1, 5.0), {}, "AO(1,5.000000)"),
    ("ao_execute", (2, 2.5), {}, "AOExecute(2,2.500000)"),
    ("brake_control", (1, 0), {}, "BrakeControl(1,0)"),
    # Multi-arg commands
    (
        "set_arm_orientation",
        (1, -1, 1, 0),
        {},
        "SetArmOrientation(1,-1,1,0)",
    ),
    (
        "get_hold_regs",
        (0, 3095, 4, "U16"),
        {},
        "GetHoldRegs(0,3095,4,U16)",
    ),
    (
        "set_terminal_485",
        (1, 9600, "8N1", 0),
        {},
        "SetTerminal485(1,9600,8N1,0)",
    ),
    (
        "modbus_create",
        ("192.168.1.100", 502, 1, 0),
        {},
        "ModbusCreate(192.168.1.100,502,1,0)",
    ),
    (
        "get_in_bits",
        (0, 1, 8),
        {},
        "GetInBits(0,1,8)",
    ),
    (
        "get_coils",
        (0, 2, 16),
        {},
        "GetCoils(0,2,16)",
    ),
    (
        "set_coils",
        (0, 2, 16, 1),
        {},
        "SetCoils(0,2,16,1)",
    ),
    # String-arg commands
    ("run_script", ("myproject",), {}, "RunScript(myproject)"),
    ("get_trace_start_pose", ("trace.traj",), {}, "GetTraceStartPose(trace.traj)"),
    ("get_path_start_pose", ("path.json",), {}, "GetPathStartPose(path.json)"),
    ("handle_traj_points", ("traj.json",), {}, "HandleTrajPoints(traj.json)"),
    # Kinematics
    (
        "positive_solution",
        (0.0, 0.0, 90.0, 0.0, 0.0, 0.0, 1, 0),
        {},
        "PositiveSolution(0.000000,0.000000,90.000000,0.000000,0.000000,0.000000,1,0)",
    ),
    (
        "set_hold_regs",
        (0, 3095, 1, "100"),
        {},
        "SetHoldRegs(0,3095,1,100)",
    ),
    (
        "set_hold_regs",
        (0, 3095, 1, "100", "U16"),
        {},
        "SetHoldRegs(0,3095,1,100,U16)",
    ),
    # vel_j / vel_l are aliases to speed_j / speed_l — they send the same string
    ("vel_j", (50,), {}, "SpeedJ(50)"),
    ("vel_l", (40,), {}, "SpeedL(40)"),
    # wait (takes int via {:d})
    ("wait", (1000,), {}, "wait(1000)"),
    # get_in_regs without extra params
    ("get_in_regs", (0, 1, 8), {}, "GetInRegs(0,1,8)"),
]


@pytest.mark.parametrize("method,args,kwargs,expected", _CMD_CASES)
def test_command_serialization(
    method: str,
    args: tuple,
    kwargs: dict,
    expected: str,
    mock_dashboard: tuple,
) -> None:
    """Calling ``method(*args, **kwargs)`` must send exactly ``expected`` string."""
    db, sent = mock_dashboard
    getattr(db, method)(*args, **kwargs)
    assert (
        sent[-1] == expected
    ), f"{method}({args}, {kwargs}) → got {sent[-1]!r}, want {expected!r}"


# ---------------------------------------------------------------------------
# enable_robot — conditional serialization
# ---------------------------------------------------------------------------


class TestEnableRobot:
    def test_no_args(self, mock_dashboard: tuple) -> None:
        db, sent = mock_dashboard
        db.enable_robot()
        assert sent[-1] == "EnableRobot()"

    def test_load_only(self, mock_dashboard: tuple) -> None:
        db, sent = mock_dashboard
        db.enable_robot(load=1.5)
        assert sent[-1] == "EnableRobot(1.500000)"

    def test_load_and_all_center(self, mock_dashboard: tuple) -> None:
        db, sent = mock_dashboard
        db.enable_robot(load=1.5, center_x=0.1, center_y=0.2, center_z=0.3)
        assert sent[-1] == "EnableRobot(1.500000,0.100000,0.200000,0.300000)"

    def test_load_without_nonzero_center(self, mock_dashboard: tuple) -> None:
        """load != 0 but all centers are 0 → only load is appended."""
        db, sent = mock_dashboard
        db.enable_robot(load=2.0)
        assert sent[-1] == "EnableRobot(2.000000)"


# ---------------------------------------------------------------------------
# set_payload — variadic params (note trailing-comma quirk)
# ---------------------------------------------------------------------------


class TestSetPayload:
    def test_single_arg(self, mock_dashboard: tuple) -> None:
        db, sent = mock_dashboard
        db.set_payload(1.5)
        assert sent[-1] == "SetPayload(1.500000)"

    def test_with_extra_param(self, mock_dashboard: tuple) -> None:
        """Extra dyn_params are appended with a trailing comma (source behaviour)."""
        db, sent = mock_dashboard
        db.set_payload(1.5, "extra")
        # Source: string + str(params) + "," + ")"
        assert sent[-1] == "SetPayload(1.500000extra,)"


# ---------------------------------------------------------------------------
# do_group — variadic, trailing-comma quirk
# ---------------------------------------------------------------------------


class TestDoGroup:
    def test_no_params(self, mock_dashboard: tuple) -> None:
        db, sent = mock_dashboard
        db.do_group()
        assert sent[-1] == "DOGroup()"

    def test_with_params(self, mock_dashboard: tuple) -> None:
        db, sent = mock_dashboard
        db.do_group(1, 0, 2, 1)
        assert sent[-1] == "DOGroup(1,0,2,1,)"


# ---------------------------------------------------------------------------
# inverse_solution — variadic params use repr() directly (no comma prefix)
# ---------------------------------------------------------------------------


class TestInverseSolution:
    def test_no_dyn_params(self, mock_dashboard: tuple) -> None:
        db, sent = mock_dashboard
        db.inverse_solution(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0)
        assert (
            sent[-1]
            == "InverseSolution(0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0,0)"
        )
