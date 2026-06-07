"""Unit tests for DobotRobot protocol-specific method guards."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest


class _DummyDashboard:
    """A dashboard mock that accepts any method call."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def __getattr__(self, name: str):
        def handler(*args, **kwargs):
            self.calls.append(name)
            return f"ok:{name}"

        return handler


class _DummyMotion:
    """A motion backend mock that accepts any method call."""

    def __init__(self) -> None:
        self.calls: list[str] = []
        self.has_servo_js = False

    def __getattr__(self, name: str):
        def handler(*args, **kwargs):
            self.calls.append(name)
            return f"ok:{name}"

        return handler


def _make_robot(protocol: str, monkeypatch: pytest.MonkeyPatch):
    """Build a DobotRobot with dummy backends."""
    import dobot_api.error_monitor as em
    import dobot_api.robot as robot_module

    dashboard = _DummyDashboard()
    motion = _DummyMotion()
    dashboard.motion_calls = motion.calls  # alias for assertions

    if protocol == "v3":
        import dobot_api.v3 as v3_mod

        monkeypatch.setattr(v3_mod, "DobotApiDashboard", lambda ip, port: dashboard)
        monkeypatch.setattr(v3_mod, "DobotApiMove", lambda ip, port: motion)
    else:
        import dobot_api.v4 as v4_mod

        monkeypatch.setattr(v4_mod, "DobotApiDashboard", lambda ip, port: dashboard)
        # For v4, dashboard IS the motion backend

    monkeypatch.setattr(
        em,
        "RobotErrorMonitor",
        lambda dashboard_or_ip, protocol: SimpleNamespace(
            check_errors=lambda language="en": False,
            clear_robot_error=lambda language="en": True,
        ),
    )

    robot = robot_module.DobotRobot("192.168.1.6", protocol=protocol)
    # Override for v4: both dashboard and _motion_backend point to dashboard
    if protocol == "v4":
        robot._motion_backend = dashboard
    return robot, dashboard, motion


# ---------------------------------------------------------------------------
# V3-only commands -> NotImplementedError on V4
# ---------------------------------------------------------------------------


class TestV3OnlyCommandsRaiseOnV4:
    V3_ONLY_METHODS = [
        "rel_mov_l",
        "rel_mov_j_tool",
        "rel_mov_l_tool",
        "rel_mov_j_user",
        "rel_mov_l_user",
        "rel_joint_mov_j",
        "sync",
        "start_trace",
        "start_path",
        "start_fc_trace",
        "arch",
        "lim_z",
        "set_arm_orientation",
        "pause",
        "resume",
        "wait",
    ]

    @pytest.mark.parametrize("method_name", V3_ONLY_METHODS)
    def test_raises_not_implemented_on_v4(
        self, method_name: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        robot, _, _ = _make_robot("v4", monkeypatch)
        method = getattr(robot, method_name)
        with pytest.raises(NotImplementedError, match="not available on V4"):
            method(1, 2, 3, 4, 5, 6)

    @pytest.mark.parametrize("method_name", V3_ONLY_METHODS)
    def test_routes_to_backend_on_v3(
        self, method_name: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        robot, dashboard, motion = _make_robot("v3", monkeypatch)
        method = getattr(robot, method_name)
        result = method(1, 2, 3, 4, 5, 6)
        assert result is not None


class TestV3OnlyMotionCommands:
    """Verify V3-only motion commands route to _motion_backend on V3."""

    def test_rel_mov_l_routes_to_motion(self, monkeypatch: pytest.MonkeyPatch) -> None:
        robot, dashboard, motion = _make_robot("v3", monkeypatch)
        robot.rel_mov_l(1, 2, 3)
        assert "rel_mov_l" in motion.calls

    def test_sync_routes_to_motion(self, monkeypatch: pytest.MonkeyPatch) -> None:
        robot, dashboard, motion = _make_robot("v3", monkeypatch)
        robot.sync()
        assert "sync" in motion.calls


# ---------------------------------------------------------------------------
# V4-only commands -> NotImplementedError on V3
# ---------------------------------------------------------------------------


class TestV4OnlyCommandsRaiseOnV3:
    V4_ONLY_METHODS = [
        "mov_j_io",
        "mov_l_io",
        "arc_io",
        "circle",
        "fc_force_mode",
        "fc_off",
        "fc_set_deviation",
        "fc_set_force_limit",
        "fc_set_mass",
        "fc_set_stiffness",
        "fc_set_damping",
        "enable_ft_sensor",
        "force_drive_mode",
        "cnv_init",
        "cnv_mov_l",
        "arc_track_start",
        "arc_track_end",
        "weave_start",
        "check_mov_j",
        "check_mov_l",
    ]

    @pytest.mark.parametrize("method_name", V4_ONLY_METHODS)
    def test_raises_not_implemented_on_v3(
        self, method_name: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        robot, _, _ = _make_robot("v3", monkeypatch)
        method = getattr(robot, method_name)
        # circle requires 13 args; other methods are flexible
        if method_name == "circle":
            args: tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1)
        else:
            args = (1, 2, 3, 4, 5, 6)
        with pytest.raises(NotImplementedError, match="not available on V3"):
            method(*args)


# ---------------------------------------------------------------------------
# Shared motion commands
# ---------------------------------------------------------------------------


class TestSharedMotionCommands:
    def test_servo_j_delegates(self, monkeypatch: pytest.MonkeyPatch) -> None:
        robot, dashboard, motion = _make_robot("v3", monkeypatch)
        robot.servo_j(1, 2, 3, 4, 5, 6)
        assert "servo_j" in motion.calls

    def test_servo_p_delegates(self, monkeypatch: pytest.MonkeyPatch) -> None:
        robot, dashboard, motion = _make_robot("v3", monkeypatch)
        robot.servo_p(100, 200, 300, 0, 0, 0)
        assert "servo_p" in motion.calls

    def test_arc_delegates(self, monkeypatch: pytest.MonkeyPatch) -> None:
        robot, dashboard, motion = _make_robot("v3", monkeypatch)
        robot.arc(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        assert "arc" in motion.calls

    def test_move_jog_delegates(self, monkeypatch: pytest.MonkeyPatch) -> None:
        robot, dashboard, motion = _make_robot("v3", monkeypatch)
        robot.move_jog("j1+")
        assert "move_jog" in motion.calls


# ---------------------------------------------------------------------------
# Deprecated aliases
# ---------------------------------------------------------------------------


class TestDeprecatedAliases:
    def test_speed_j_emits_warning_and_delegates_to_vel_j(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        robot, dashboard, _ = _make_robot("v4", monkeypatch)
        with pytest.warns(DeprecationWarning, match="speed_j"):
            robot.speed_j(50)
        assert "vel_j" in dashboard.calls or "speed_j" in dashboard.calls

    def test_speed_l_emits_warning_and_delegates_to_vel_l(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        robot, dashboard, _ = _make_robot("v4", monkeypatch)
        with pytest.warns(DeprecationWarning, match="speed_l"):
            robot.speed_l(50)
        assert "vel_l" in dashboard.calls or "speed_l" in dashboard.calls


# ---------------------------------------------------------------------------
# __getattr__ fallback
# ---------------------------------------------------------------------------


class TestGetattrFallback:
    def test_unknown_dashboard_method_routes_via_getattr(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        robot, dashboard, _ = _make_robot("v4", monkeypatch)
        result = robot.get_pose()
        assert "get_pose" in dashboard.calls

    def test_unknown_method_raises_attribute_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A truly unknown method must raise AttributeError."""
        import dobot_api.robot as robot_module
        import dobot_api.error_monitor as em
        import dobot_api.v4 as v4_mod

        # Use a plain object (not MagicMock) so that hasattr is truthful
        class _StrictDashboard:
            ip = "192.168.1.6"

            def get_pose(self):
                return "pose"

            def close(self):
                pass

            def reconnect(self):
                pass

        strict = _StrictDashboard()
        monkeypatch.setattr(v4_mod, "DobotApiDashboard", lambda ip, port: strict)
        monkeypatch.setattr(
            em,
            "RobotErrorMonitor",
            lambda dashboard_or_ip, protocol: SimpleNamespace(
                check_errors=lambda language="en": False,
                clear_robot_error=lambda language="en": True,
            ),
        )

        robot = robot_module.DobotRobot("192.168.1.6", protocol="v4")
        robot._motion_backend = strict
        with pytest.raises(AttributeError):
            robot.nonexistent_method_xyz()

    def test_move_property_emits_deprecation_warning(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        robot, dashboard, _ = _make_robot("v4", monkeypatch)
        with pytest.warns(DeprecationWarning, match="DobotRobot.move is deprecated"):
            _ = robot.move
