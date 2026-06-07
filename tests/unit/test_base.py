"""Unit tests for the shared DobotApi base class (V3+V4 union)."""

from __future__ import annotations

import socket
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from dobot_api.base import DobotApi


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_socket() -> Generator[MagicMock, None, None]:
    """Patch socket.socket so no real TCP connection is attempted."""
    with patch("socket.socket", autospec=True) as mock_sock_cls:
        mock_instance = MagicMock()
        mock_sock_cls.return_value = mock_instance
        yield mock_instance


# ---------------------------------------------------------------------------
# Port whitelist
# ---------------------------------------------------------------------------


class TestPortWhitelist:
    VALID_PORTS = [29999, 30003, 30004, 30005, 30006]
    INVALID_PORTS = [80, 443, 8080, 0, 65535, 29998, 30007]

    @pytest.mark.parametrize("port", VALID_PORTS)
    def test_valid_ports_accepted(self, port: int, mock_socket: MagicMock) -> None:
        api = DobotApi("192.168.1.6", port)
        assert api.port == port
        assert api.ip == "192.168.1.6"

    @pytest.mark.parametrize("port", INVALID_PORTS)
    def test_invalid_ports_rejected(self, port: int, mock_socket: MagicMock) -> None:
        with pytest.raises(ValueError, match="Invalid port"):
            DobotApi("192.168.1.6", port)


# ---------------------------------------------------------------------------
# Connection lifecycle
# ---------------------------------------------------------------------------


class TestConnectionLifecycle:
    def test_socket_created_and_connected(self, mock_socket: MagicMock) -> None:
        api = DobotApi("192.168.1.6", 29999)
        mock_socket.connect.assert_called_once_with(("192.168.1.6", 29999))
        assert api.socket_dobot is mock_socket

    def test_sets_rcvbuf(self, mock_socket: MagicMock) -> None:
        DobotApi("192.168.1.6", 29999)
        mock_socket.setsockopt.assert_called_with(
            socket.SOL_SOCKET, socket.SO_RCVBUF, 144000
        )

    def test_close_shuts_down_and_clears(self, mock_socket: MagicMock) -> None:
        api = DobotApi("192.168.1.6", 29999)
        api.close()
        mock_socket.shutdown.assert_called_once_with(socket.SHUT_RDWR)
        mock_socket.close.assert_called_once()
        assert api.socket_dobot is None

    def test_close_when_already_closed_is_safe(self, mock_socket: MagicMock) -> None:
        api = DobotApi("192.168.1.6", 29999)
        api.close()
        api.close()  # must not raise

    def test_context_manager_closes_on_exit(self, mock_socket: MagicMock) -> None:
        with DobotApi("192.168.1.6", 29999) as api:
            assert api.socket_dobot is mock_socket
        mock_socket.shutdown.assert_called_once()

    def test_del_cleans_up(self, mock_socket: MagicMock) -> None:
        api = DobotApi("192.168.1.6", 29999)
        api.__del__()
        mock_socket.shutdown.assert_called_once()


# ---------------------------------------------------------------------------
# send_data / wait_reply / send_recv_msg
# ---------------------------------------------------------------------------


class TestSendRecv:
    def test_send_data_encodes_and_sends(self, mock_socket: MagicMock) -> None:
        api = DobotApi("192.168.1.6", 29999)
        api.send_data("EnableRobot()")
        mock_socket.send.assert_called_with(b"EnableRobot()")

    def test_wait_reply_decodes_response(self, mock_socket: MagicMock) -> None:
        mock_socket.recv.return_value = b"0,{},EnableRobot();"
        api = DobotApi("192.168.1.6", 29999)
        result = api.wait_reply()
        assert result == "0,{},EnableRobot();"

    def test_send_recv_msg_is_atomic(self, mock_socket: MagicMock) -> None:
        mock_socket.recv.return_value = b"0,{42},RobotMode();"
        api = DobotApi("192.168.1.6", 29999)
        result = api.send_recv_msg("RobotMode()")
        assert result == "0,{42},RobotMode();"
        mock_socket.send.assert_called_with(b"RobotMode()")
        mock_socket.recv.assert_called_once()


# ---------------------------------------------------------------------------
# Reconnect
# ---------------------------------------------------------------------------


class TestReconnect:
    def test_reconnect_returns_new_socket(self, mock_socket: MagicMock) -> None:
        api = DobotApi("192.168.1.6", 29999)
        new_sock = MagicMock()
        with patch("socket.socket", return_value=new_sock):
            result = api.reconnect()
        assert result is new_sock

    def test_reconnect_with_custom_ip_port(self, mock_socket: MagicMock) -> None:
        api = DobotApi("192.168.1.6", 29999)
        new_sock = MagicMock()
        with patch("socket.socket", return_value=new_sock):
            result = api.reconnect(ip="10.0.0.1", port=30003)
        new_sock.connect.assert_called_with(("10.0.0.1", 30003))
        assert result is new_sock


# ---------------------------------------------------------------------------
# ConnectionError propagation
# ---------------------------------------------------------------------------


class TestConnectionError:
    def test_connection_refused_raises_connection_error(self) -> None:
        with patch("socket.socket") as mock_sock_cls:
            mock_sock_cls.return_value.connect.side_effect = OSError(
                "Connection refused"
            )
            with pytest.raises(ConnectionError, match="Unable to establish"):
                DobotApi("192.168.1.6", 29999)
