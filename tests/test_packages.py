import dobot_api
import dobot_api_v3


def test_package_exports_clean_break():
    assert hasattr(dobot_api, "DobotApiDashboard")
    assert hasattr(dobot_api, "DobotApiFeedBack")
    assert not hasattr(dobot_api, "DobotApiMove")
    assert not hasattr(dobot_api, "alarmAlarmJsonFile")


def test_alias_package_exports():
    assert dobot_api_v3.DobotApiDashboard is dobot_api.DobotApiDashboard
    assert dobot_api_v3.DobotApiFeedBack is dobot_api.DobotApiFeedBack
