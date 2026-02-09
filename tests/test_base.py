import types

from dobot_api.base import DobotApi


class FakeSocket:
    def __init__(self):
        self.connected = None
        self.sent = b""
        self.closed = False

    def connect(self, endpoint):
        self.connected = endpoint

    def send(self, data):
        self.sent = data

    def recv(self, _):
        return b"OK"

    def close(self):
        self.closed = True


def test_base_connects_to_supported_port(monkeypatch):
    fake = FakeSocket()
    monkeypatch.setattr("dobot_api.base.socket.socket", lambda: fake)
    api = DobotApi("127.0.0.1", 29999)
    assert fake.connected == ("127.0.0.1", 29999)
    api.close()
    assert fake.closed


def test_base_rejects_unsupported_port():
    try:
        DobotApi("127.0.0.1", 12345)
    except ValueError as exc:
        assert "Unsupported" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_send_recv(monkeypatch):
    fake = FakeSocket()
    monkeypatch.setattr("dobot_api.base.socket.socket", lambda: fake)
    api = DobotApi("127.0.0.1", 29999)
    res = api.sendRecvMsg("RobotMode()")
    assert fake.sent == b"RobotMode()"
    assert res == "OK"
