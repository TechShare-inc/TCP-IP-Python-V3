"""Unit tests for the unified DobotRobot facade."""

from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pytest


class _Endpoint:
    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port
        self.calls: list[tuple[str, tuple[object, ...], dict[str, object]]] = []
        self.closed = False

    def close(self) -> None:
        self.closed = True

    def reconnect(self) -> None:
        self.calls.append(("reconnect", (), {}))

    def clear_error(self):
        self.calls.append(("clear_error", (), {}))
        return "0,0,ok;"

    def enable_robot(self, *args, **kwargs):
        self.calls.append(("enable_robot", args, kwargs))
        return "0,0,ok;"

    def vel_j(self, *args, **kwargs):
        self.calls.append(("vel_j", args, kwargs))
        return "0,0,ok;"

    def speed_j(self, *args, **kwargs):
        self.calls.append(("speed_j", args, kwargs))
        return "0,0,ok;"

    def mov_j(self, *args, **kwargs):
        self.calls.append(("mov_j", args, kwargs))
        return "0,0,ok;"

    def mov_l(self, *args, **kwargs):
        self.calls.append(("mov_l", args, kwargs))
        return "0,0,ok;"

    def joint_mov_j(self, *args, **kwargs):
        self.calls.append(("joint_mov_j", args, kwargs))
        return "0,0,ok;"

    def rel_mov_j(self, *args, **kwargs):
        self.calls.append(("rel_mov_j", args, kwargs))
        return "0,0,ok;"

    def servo_j(self, *args, **kwargs):
        self.calls.append(("servo_j", args, kwargs))
        return "0,0,ok;"

def test_v3_constructor_uses_dashboard_and_motion_ports(monkeypatch):
    import dobot_api.v3 as v3
    from dobot_api import DobotRobot

    created: list[_Endpoint] = []

    def factory(ip: str, port: int) -> _Endpoint:
        endpoint = _Endpoint(ip, port)
        created.append(endpoint)
        return endpoint

    monkeypatch.setattr(v3, "DobotApiDashboard", factory)
    monkeypatch.setattr(v3, "DobotApiMove", factory)
    monkeypatch.setattr(v3, "RobotErrorMonitor", lambda dashboard: SimpleNamespace())

    robot = DobotRobot("192.168.1.6", protocol="v3")

    assert robot.dashboard.port == 29999
    assert robot._motion_backend.port == 30003
    assert [endpoint.port for endpoint in created] == [29999, 30003]


def test_v4_constructor_uses_dashboard_for_motion(monkeypatch):
    import dobot_api.robot as robot_module
    import dobot_api.v4 as v4
    from dobot_api import DobotRobot

    monkeypatch.setattr(v4, "DobotApiDashboard", _Endpoint)
    monkeypatch.setattr(
        robot_module,
        "RobotErrorMonitor",
        lambda dashboard, protocol: SimpleNamespace(check_errors=lambda language="en": False),
    )

    robot = DobotRobot("192.168.1.6", protocol="v4")

    assert robot.dashboard.port == 29999
    assert robot._motion_backend is robot.dashboard


def test_v3_motion_dispatches_to_move_port(monkeypatch):
    import dobot_api.v3 as v3
    from dobot_api import DobotRobot

    monkeypatch.setattr(v3, "DobotApiDashboard", _Endpoint)
    monkeypatch.setattr(v3, "DobotApiMove", _Endpoint)
    monkeypatch.setattr(v3, "RobotErrorMonitor", lambda dashboard: SimpleNamespace())

    robot = DobotRobot("192.168.1.6", protocol="v3")
    robot.mov_j(1, 2, 3, 4, 5, 6)
    robot.mov_j(1, 2, 3, 4, 5, 6, coordinate_mode=1)

    assert robot._motion_backend.calls[0][0] == "mov_j"
    assert robot._motion_backend.calls[1][0] == "joint_mov_j"
    assert robot.dashboard.calls == []


def test_v4_motion_dispatches_to_dashboard(monkeypatch):
    import dobot_api.robot as robot_module
    import dobot_api.v4 as v4
    from dobot_api import DobotRobot

    monkeypatch.setattr(v4, "DobotApiDashboard", _Endpoint)
    monkeypatch.setattr(
        robot_module,
        "RobotErrorMonitor",
        lambda dashboard, protocol: SimpleNamespace(check_errors=lambda language="en": False),
    )

    robot = DobotRobot("192.168.1.6", protocol="v4")
    robot.mov_l(1, 2, 3, 4, 5, 6)
    robot.servo_js(1, 2, 3, 4, 5, 6)

    assert robot.dashboard.calls[0] == ("mov_l", (1, 2, 3, 4, 5, 6, 0), {})
    assert robot.dashboard.calls[1][0] == "servo_j"


def test_unsupported_v4_specific_command_errors(monkeypatch):
    import dobot_api.robot as robot_module
    import dobot_api.v4 as v4
    from dobot_api import DobotRobot

    monkeypatch.setattr(v4, "DobotApiDashboard", _Endpoint)
    monkeypatch.setattr(
        robot_module,
        "RobotErrorMonitor",
        lambda dashboard, protocol: SimpleNamespace(check_errors=lambda language="en": False),
    )

    robot = DobotRobot("192.168.1.6", protocol="v4")

    with pytest.raises(NotImplementedError):
        robot.rel_mov_j(1, 2, 3, 4, 5, 6)


def test_feedback_data_normalization() -> None:
    from dobot_api.dtypes import FeedbackData

    raw = np.zeros(1, dtype=[("test_value", "<u8"), ("q_actual", "<f8", (6,))])
    raw["test_value"][0] = 0x123456789ABCDEF
    raw["q_actual"][0] = [1, 2, 3, 4, 5, 6]

    data = FeedbackData.from_numpy(raw)

    assert data is not None
    assert data.test_value == 0x123456789ABCDEF
    np.testing.assert_array_equal(data.q_actual, [1, 2, 3, 4, 5, 6])
