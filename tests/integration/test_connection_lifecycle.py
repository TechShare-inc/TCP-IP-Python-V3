"""Integration tests — TCP connection lifecycle (connect, close, reconnect)."""

from __future__ import annotations

import pytest

from tests.integration.conftest import _AnyPortApi, make_api
from tests.integration.stub_server import StubServer

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# Basic connect / close
# ---------------------------------------------------------------------------


class TestBasicConnectClose:
    def test_connects_to_stub_server(self, stub: StubServer) -> None:
        api = make_api(stub)
        assert api.socket_dobot is not None
        api.close()

    def test_close_sets_socket_none(self, stub: StubServer) -> None:
        api = make_api(stub)
        api.close()
        assert api.socket_dobot is None

    def test_send_recv_msg_returns_string(self, stub: StubServer) -> None:
        api = make_api(stub)
        result = api.send_recv_msg("DisableRobot()")
        assert isinstance(result, str)
        api.close()

    def test_send_recv_msg_contains_command_echo(self, stub: StubServer) -> None:
        api = make_api(stub)
        result = api.send_recv_msg("GetPose()")
        assert "GetPose()" in result
        api.close()


# ---------------------------------------------------------------------------
# Repeated connect / close — socket leak detection
# ---------------------------------------------------------------------------


class TestRepeatedConnectClose:
    def test_100_connect_close_cycles_no_exception(self, stub: StubServer) -> None:
        """100 connect/close cycles must complete without raising."""
        errors = []
        for _ in range(100):
            try:
                api = make_api(stub)
                api.close()
            except Exception as exc:
                errors.append(exc)
        assert not errors, f"Errors during connect/close cycles: {errors}"


# ---------------------------------------------------------------------------
# Reconnect
# ---------------------------------------------------------------------------


class TestReconnect:
    def test_reconnect_allows_further_communication(self, stub: StubServer) -> None:
        api = make_api(stub)
        api.reconnect()
        result = api.send_recv_msg("RobotMode()")
        assert isinstance(result, str)
        api.close()

    def test_reconnect_after_manual_socket_close(self, stub: StubServer) -> None:
        """Simulates the socket being closed externally; reconnect should recover."""
        api = make_api(stub)
        # Force-close the socket without going through api.close()
        api.socket_dobot.close()  # type: ignore[union-attr]
        api.socket_dobot = None
        api.reconnect()
        assert api.socket_dobot is not None
        api.close()


# ---------------------------------------------------------------------------
# Connection refused
# ---------------------------------------------------------------------------


class TestConnectionRefused:
    def test_connect_to_closed_port_raises_connection_error(self) -> None:
        with pytest.raises(
            ConnectionError, match="Unable to establish socket connection"
        ):
            _AnyPortApi("127.0.0.1", 19999)  # nothing listening there
