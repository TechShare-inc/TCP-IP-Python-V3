from dobot_api.dashboard import DobotApiDashboard


def _dashboard_without_socket():
    dash = DobotApiDashboard.__new__(DobotApiDashboard)
    dash.socket_dobot = None
    dash.sendRecvMsg = lambda cmd: cmd
    return dash


def test_build_cmd_helper():
    dash = _dashboard_without_socket()
    cmd = dash._build_cmd("Cmd", 1, 2.0, arr=[1, 2])
    assert cmd == "Cmd(1,2.000000,arr={1,2})"


def test_control_and_motion_command_serialization():
    dash = _dashboard_without_socket()
    assert dash.EnableRobot() == "EnableRobot()"
    assert dash.SpeedFactor(50) == "SpeedFactor(50)"
    assert dash.MovJ(1, 2, 3, 4, 5, 6) == "MovJ(1.000000,2.000000,3.000000,4.000000,5.000000,6.000000)"
    assert dash.MovL(1, 2, 3, 4, 5, 6) == "MovL(1.000000,2.000000,3.000000,4.000000,5.000000,6.000000)"


def test_v4_style_aliases():
    dash = _dashboard_without_socket()
    assert dash.VelJ(30) == "SpeedJ(30)"
    assert dash.VelL(40) == "SpeedL(40)"
