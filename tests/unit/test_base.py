"""Unit tests for DobotApi base class (networking, locking, lifecycle)."""

from __future__ import annotations

import threading
from unittest.mock import MagicMock

import pytest

from dobot_api_v3.base import DobotApi

pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# Port validation
# ---------------------------------------------------------------------------


class TestPortValidation:
    """The port whitelist rejects everything outside the five approved ports."""

    @pytest.mark.parametrize("port", [29999, 30003, 30004, 30005, 30006])
    def test_valid_port_accepted(self, port: int, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_sock = MagicMock()
        monkeypatch.setattr("socket.socket", mock_sock)
        DobotApi("127.0.0.1", port)
        mock_sock.return_value.connect.assert_called_once_with(("127.0.0.1", port))

    @pytest.mark.parametrize("port", [80, 8080, 30000, 29998, 30007, 0, -1])
    def test_invalid_port_raises_value_error(
        self, port: int, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr("socket.socket", MagicMock())
        with pytest.raises(ValueError, match="Unsupported Dobot TCP port"):
            DobotApi("127.0.0.1", port)


# ---------------------------------------------------------------------------
# Connection error handling
# ---------------------------------------------------------------------------


class TestConnectError:
    def test_oserror_wrapped_as_connection_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_sock = MagicMock()
        mock_sock.return_value.connect.side_effect = OSError("connection refused")
        monkeypatch.setattr("socket.socket", mock_sock)
        with pytest.raises(
            ConnectionError, match="Unable to establish socket connection"
        ):
            DobotApi("127.0.0.1", 29999)


# ---------------------------------------------------------------------------
# send_data
# ---------------------------------------------------------------------------


class TestSendData:
    def test_encodes_utf8_and_calls_socket_send(self, mock_base: DobotApi) -> None:
        mock_base.send_data("EnableRobot()")
        mock_base.socket_dobot.send.assert_called_once_with(b"EnableRobot()")  # type: ignore[union-attr]

    def test_unicode_command_encoded_correctly(self, mock_base: DobotApi) -> None:
        mock_base.send_data("RunScript(test_\u6587\u4ef6)")
        expected = "RunScript(test_\u6587\u4ef6)".encode("utf-8")
        mock_base.socket_dobot.send.assert_called_once_with(expected)  # type: ignore[union-attr]

    def test_raises_runtime_error_when_socket_is_none(
        self, mock_base: DobotApi
    ) -> None:
        mock_base.socket_dobot = None
        with pytest.raises(RuntimeError, match="Socket connection is not established"):
            mock_base.send_data("EnableRobot()")


# ---------------------------------------------------------------------------
# wait_reply
# ---------------------------------------------------------------------------


class TestWaitReply:
    def test_reads_1024_bytes_and_decodes_utf8(self, mock_base: DobotApi) -> None:
        mock_base.socket_dobot.recv.return_value = b"0,0,ok;"  # type: ignore[union-attr]
        result = mock_base.wait_reply()
        mock_base.socket_dobot.recv.assert_called_once_with(1024)  # type: ignore[union-attr]
        assert result == "0,0,ok;"

    def test_empty_response_returns_empty_string(self, mock_base: DobotApi) -> None:
        mock_base.socket_dobot.recv.return_value = b""  # type: ignore[union-attr]
        assert mock_base.wait_reply() == ""

    def test_raises_runtime_error_when_socket_is_none(
        self, mock_base: DobotApi
    ) -> None:
        mock_base.socket_dobot = None
        with pytest.raises(RuntimeError, match="Socket connection is not established"):
            mock_base.wait_reply()


# ---------------------------------------------------------------------------
# send_recv_msg — thread-safety
# ---------------------------------------------------------------------------


class TestSendRecvMsg:
    def test_returns_decoded_response(self, mock_base: DobotApi) -> None:
        mock_base.socket_dobot.recv.return_value = b"0,0,result;"  # type: ignore[union-attr]
        result = mock_base.send_recv_msg("GetPose()")
        assert result == "0,0,result;"

    def test_lock_is_held_during_send_and_recv(
        self, mock_base: DobotApi, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """lock.acquire must be called before send and lock.release after recv."""
        mock_base.socket_dobot.recv.return_value = b"ok"  # type: ignore[union-attr]
        call_order: list[str] = []

        real_lock = threading.Lock()

        class TrackedLock:
            """A Python-level lock wrapper that records acquire/release calls.

            C-extension ``_thread.lock`` attributes are read-only so we cannot
            patch ``acquire``/``release`` individually.  Replacing the entire
            ``_global_lock`` with this wrapper sidesteps that limitation.
            """

            def __enter__(self) -> TrackedLock:
                call_order.append("acquire")
                real_lock.acquire()
                return self

            def __exit__(self, *args: object) -> None:
                call_order.append("release")
                real_lock.release()

        monkeypatch.setattr(mock_base, "_global_lock", TrackedLock())

        mock_base.send_recv_msg("test()")

        assert call_order[0] == "acquire"
        assert call_order[-1] == "release"


# ---------------------------------------------------------------------------
# close
# ---------------------------------------------------------------------------


class TestClose:
    def test_close_calls_socket_close(self, mock_base: DobotApi) -> None:
        sock = mock_base.socket_dobot
        mock_base.close()
        sock.close.assert_called_once()  # type: ignore[union-attr]

    def test_close_sets_socket_to_none(self, mock_base: DobotApi) -> None:
        mock_base.close()
        assert mock_base.socket_dobot is None

    def test_close_when_already_none_is_idempotent(self, mock_base: DobotApi) -> None:
        mock_base.socket_dobot = None
        mock_base.close()  # must not raise


# ---------------------------------------------------------------------------
# reconnect
# ---------------------------------------------------------------------------


class TestReconnect:
    def test_calls_close_then_connect(
        self, mock_base: DobotApi, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        close_spy = MagicMock()
        connect_spy = MagicMock()
        monkeypatch.setattr(mock_base, "close", close_spy)
        monkeypatch.setattr(mock_base, "_connect", connect_spy)
        mock_base.reconnect()
        close_spy.assert_called_once()
        connect_spy.assert_called_once()
