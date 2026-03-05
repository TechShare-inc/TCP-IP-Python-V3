"""Base TCP communication class for Dobot API.

Data-type definitions (``FeedbackDtype``, ``FeedbackData``,
``PROTOCOL_FIELD_MAP``) have been extracted to :mod:`dobot_api_v3.dtypes`.
They are re-exported here for backward compatibility so that existing code
doing ``from dobot_api_v3.base import FeedbackDtype`` continues to work.
"""

from __future__ import annotations

import socket
import threading
from typing import Optional

from loguru import logger

__all__ = [
    "DobotApi",
]


class DobotApi:
    """Base TCP communication class for Dobot TCP API ports.

    This class provides connection lifecycle management, message send/receive
    helpers, and thread-safe request/response behavior for the dashboard,
    movement, and feedback sockets.
    """

    def __init__(self, ip: str, port: int) -> None:
        """Initialize and connect a Dobot TCP socket.

        Args:
            ip: Robot controller IP address.
            port: Robot TCP port. Supported ports are 29999, 30003, 30004,
                30005, and 30006.

        Raises:
            ValueError: If ``port`` is not a supported Dobot TCP port.
            ConnectionError: If the socket connection fails.
        """
        self.ip = ip
        self.port = port
        self.socket_dobot: Optional[socket.socket] = None
        self._global_lock = threading.Lock()
        self._connect()

    def _connect(self) -> None:
        """Open a socket connection to the configured endpoint.

        Raises:
            ValueError: If ``self.port`` is not a supported Dobot TCP port.
            ConnectionError: If the socket connection cannot be established.
        """
        if self.port not in (29999, 30003, 30004, 30005, 30006):
            raise ValueError(f"Unsupported Dobot TCP port: {self.port}")
        try:
            self.socket_dobot = socket.socket()
            self.socket_dobot.connect((self.ip, self.port))
        except OSError as exc:
            raise ConnectionError(
                f"Unable to establish socket connection to {self.ip}:{self.port}"
            ) from exc

    def reconnect(self) -> None:
        """Reconnect the socket to the original endpoint.

        Raises:
            ValueError: If ``self.port`` is invalid.
            ConnectionError: If reconnection fails.
        """
        self.close()
        self._connect()

    def log(self, text: str) -> None:
        """Write a log message using the project logger.

        Args:
            text: Message to emit.
        """
        logger.info(text)

    def send_data(self, string: str) -> None:
        """Send a UTF-8 command string to the robot.

        Args:
            string: Command string to send.

        Raises:
            RuntimeError: If the socket is not connected.
        """
        if self.socket_dobot is None:
            raise RuntimeError("Socket connection is not established")
        self.log(f"Send to {self.ip}:{self.port}: {string}")
        self.socket_dobot.send(string.encode("utf-8"))

    def wait_reply(self) -> str:
        """Receive and decode one robot reply frame.

        Accumulates data from the socket until the Dobot protocol terminator
        (``;``) is found, handling responses that arrive across multiple TCP
        segments.

        Returns:
            UTF-8 decoded response string, or an empty string if the
            connection is closed before any data arrives.

        Raises:
            RuntimeError: If the socket is not connected.
        """
        if self.socket_dobot is None:
            raise RuntimeError("Socket connection is not established")
        data = b""
        while True:
            chunk = self.socket_dobot.recv(1024)
            if not chunk:
                break
            data += chunk
            if b";" in chunk:
                break
        data_str = data.decode("utf-8") if data else ""
        self.log(f"Receive from {self.ip}:{self.port}: {data_str}")
        return data_str

    def send_recv_msg(self, string: str) -> str:
        """Send one command and wait for one reply atomically.

        Args:
            string: Command string to send.

        Returns:
            Decoded robot response string.

        Raises:
            RuntimeError: If the socket is not connected.
        """
        with self._global_lock:
            self.send_data(string)
            return self.wait_reply()

    def __enter__(self) -> "DobotApi":
        """Support ``with DobotApi(...) as api:`` usage."""
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_val: object,
        exc_tb: object,
    ) -> None:
        """Close the socket when exiting the ``with`` block."""
        self.close()

    def close(self) -> None:
        """Close the socket if connected."""
        if self.socket_dobot is not None:
            self.socket_dobot.close()
            self.socket_dobot = None

    def __del__(self) -> None:
        self.close()
