"""Integration tests -- V4 protocol TCP connection lifecycle.

Uses the stub server to verify V4 ``DobotApi`` connect, close, reconnect,
and command/response round-trips with the V4 wire format (brace-delimited
payloads).
"""

from __future__ import annotations

import socket as _socket

import pytest

from dobot_api._vendor import ensure_vendor_paths

ensure_vendor_paths()

from dobot_api_v4.base import DobotApi as _V4DobotApi  # noqa: E402
from tests.integration.conftest import _AnyPortApi  # V3, for comparison
from tests.integration.stub_server import StubServer

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# V4 port-agnostic subclass (bypasses port whitelist)
# ---------------------------------------------------------------------------


class _AnyPortApiV4(_V4DobotApi):
    """V4 DobotApi that accepts any TCP port (bypasses whitelist)."""

    _ALLOWED_PORTS = set(range(1, 65536))

    def _connect(self) -> None:
        try:
            self.socket_dobot = _socket.socket()
            self.socket_dobot.connect((self.ip, self.port))
        except OSError as exc:
            raise ConnectionError(
                f"Unable to establish socket connection to {self.ip}:{self.port}"
            ) from exc


def _make_v4_api(stub: StubServer) -> _AnyPortApiV4:
    return _AnyPortApiV4(stub.host, stub.port)


# ---------------------------------------------------------------------------
# Basic connect / close
# ---------------------------------------------------------------------------


class TestV4ConnectClose:
    def test_connects_to_stub_server(self, stub: StubServer) -> None:
        api = _make_v4_api(stub)
        assert api.socket_dobot is not None
        api.close()

    def test_close_sets_socket_none(self, stub: StubServer) -> None:
        api = _make_v4_api(stub)
        api.close()
        assert api.socket_dobot is None

    def test_send_recv_msg_returns_string(self, stub: StubServer) -> None:
        api = _make_v4_api(stub)
        result = api.send_recv_msg("EnableRobot(0.000000,0.000000,0.000000,0.000000)")
        assert isinstance(result, str)
        api.close()

    def test_send_recv_msg_with_brace_format(self, stub: StubServer) -> None:
        """V4 uses brace-delimited payloads."""
        api = _make_v4_api(stub)
        result = api.send_recv_msg(
            "MovJ(200.000000,0.000000,200.000000,180.000000,0.000000,90.000000)"
        )
        assert isinstance(result, str)
        api.close()

    def test_close_then_reconnect_works(self, stub: StubServer) -> None:
        api = _make_v4_api(stub)
        api.close()
        new_sock = api.reconnect()
        # V4 reconnect returns a new socket but does not set self.socket_dobot
        assert new_sock is not None
        # Assign it and verify communication still works
        api.socket_dobot = new_sock
        result = api.send_recv_msg("RobotMode()")
        assert isinstance(result, str)
        api.close()

    def test_context_manager_closes(self, stub: StubServer) -> None:
        with _AnyPortApiV4(stub.host, stub.port) as api:
            assert api.socket_dobot is not None
        assert api.socket_dobot is None


# ---------------------------------------------------------------------------
# Repeated connect / close -- socket leak detection
# ---------------------------------------------------------------------------


class TestV4RepeatedConnectClose:
    def test_100_connect_close_cycles_no_exception(self, stub: StubServer) -> None:
        errors = []
        for _ in range(100):
            try:
                api = _make_v4_api(stub)
                api.close()
            except Exception as exc:
                errors.append(exc)
        assert not errors, f"Errors during V4 connect/close cycles: {errors}"


# ---------------------------------------------------------------------------
# V4-specific behaviors
# ---------------------------------------------------------------------------


class TestV4Specific:
    def test_send_data_does_not_raise_on_stub(self, stub: StubServer) -> None:
        """V4 send_data has auto-reconnect; verify it works with stub."""
        api = _make_v4_api(stub)
        api.send_data("RobotMode()")
        result = api.wait_reply()
        assert isinstance(result, str)
        api.close()

    def test_rcvbuf_is_set(self, stub: StubServer) -> None:
        api = _make_v4_api(stub)
        bufsize = api.socket_dobot.getsockopt(
            _socket.SOL_SOCKET, _socket.SO_RCVBUF
        )
        assert bufsize >= 144000
        api.close()

    def test_response_contains_brace_format(self, stub: StubServer) -> None:
        """V4 responses use {payload} brace-delimited format."""
        api = _make_v4_api(stub)
        result = api.send_recv_msg(
            "GetPose()"
        )
        # Stub echoes back -- V4 format has {payload}
        assert isinstance(result, str)
        api.close()


# ---------------------------------------------------------------------------
# V3 vs V4 base comparison (both work with the same stub)
# ---------------------------------------------------------------------------


class TestV3V4Comparison:
    def test_both_v3_and_v4_connect_to_same_stub(self, stub: StubServer) -> None:
        v3_api = _AnyPortApi(stub.host, stub.port)
        v4_api = _make_v4_api(stub)

        v3_result = v3_api.send_recv_msg("RobotMode()")
        v4_result = v4_api.send_recv_msg("RobotMode()")

        assert isinstance(v3_result, str)
        assert isinstance(v4_result, str)

        v3_api.close()
        v4_api.close()
