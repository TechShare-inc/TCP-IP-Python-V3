import numpy as np

from dobot_api.feedback import DobotApiFeedBack


class FakeSocket:
    def __init__(self, payloads):
        self.payloads = payloads

    def setblocking(self, _):
        return None

    def recv(self, _):
        return self.payloads.pop(0)

    def close(self):
        return None


def test_feedback_parses_1440_packet():
    feed = DobotApiFeedBack.__new__(DobotApiFeedBack)
    feed.socket_dobot = FakeSocket([b"x" * 1440])
    data = feed.feedBackData()
    assert data is not None
    assert isinstance(data, np.ndarray)


def test_feedback_raises_when_packets_missing():
    feed = DobotApiFeedBack.__new__(DobotApiFeedBack)
    feed.socket_dobot = FakeSocket([b"x" * 100] * 10)
    try:
        feed.feedBackData()
    except RuntimeError as exc:
        assert "Missing data packets" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError")
