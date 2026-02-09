import json
from io import BytesIO

from dobot_api.error_monitor import RobotErrorMonitor


class DummyResponse:
    def __init__(self, payload: bytes):
        self.payload = payload

    def read(self):
        return self.payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_error_monitor_success(monkeypatch):
    payload = {"errMsg": [{"id": 16}]}
    data = json.dumps(payload).encode("utf-8")
    monkeypatch.setattr(
        "dobot_api.error_monitor.urllib.request.urlopen",
        lambda *args, **kwargs: DummyResponse(data),
    )
    mon = RobotErrorMonitor("127.0.0.1")
    info = mon.get_error_info(language="en")
    assert info is not None
    assert "errMsg" in info
    assert "description" in info["errMsg"][0]


def test_error_monitor_network_error(monkeypatch):
    def fail(*args, **kwargs):
        raise OSError("network")

    monkeypatch.setattr("dobot_api.error_monitor.urllib.request.urlopen", fail)
    mon = RobotErrorMonitor("127.0.0.1")
    assert mon.get_error_info(language="en") is None
