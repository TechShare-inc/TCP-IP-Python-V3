"""Base class for Dobot API TCP/IP communication."""

from __future__ import annotations

import socket
import threading
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from tkinter import Text


class DobotApi:
    """Base TCP socket communication class for Dobot robot.

    This class handles the low-level socket communication with the robot.
    It supports three ports:
        - 29999: Dashboard port (settings and control commands)
        - 30003: Move port (motion commands)
        - 30004: Feedback port (real-time state data)

    Args:
        ip: Robot IP address
        port: Connection port (29999, 30003, or 30004)
        *args: Optional Text widget for logging

    """

    DASHBOARD_PORT = 29999
    MOVE_PORT = 30003
    FEEDBACK_PORT = 30004
    VALID_PORTS = {DASHBOARD_PORT, MOVE_PORT, FEEDBACK_PORT}

    def __init__(self, ip: str, port: int, *args) -> None:
        self.ip = ip
        self.port = port
        self.socket_dobot: socket.socket | None = None
        self._global_lock = threading.Lock()
        self.text_log: Text | None = None

        if args:
            self.text_log = args[0]

        if self.port not in self.VALID_PORTS:
            raise ValueError(f"Invalid port {self.port}. Must be one of {self.VALID_PORTS}")

        try:
            self.socket_dobot = socket.socket()
            self.socket_dobot.connect((self.ip, self.port))
            logger.info(f"Connected to Dobot at {self.ip}:{self.port}")
        except OSError as e:
            logger.error(f"Failed to connect to Dobot at {self.ip}:{self.port}: {e}")
            raise ConnectionError(
                f"Unable to establish socket connection on port {self.port}"
            ) from e

    def log(self, text: str) -> None:
        """Log a message using loguru and optionally to text widget."""
        logger.debug(text)
        if self.text_log:
            from datetime import datetime
            from tkinter import END

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
            self.text_log.insert(END, date + text + "\n")

    def send_data(self, string: str) -> None:
        """Send a command string to the robot."""
        self.log(f"Send to {self.ip}:{self.port}: {string}")
        try:
            if self.socket_dobot:
                self.socket_dobot.send(str.encode(string, "utf-8"))
        except Exception as e:
            logger.error(f"Send error: {e}")

    def wait_reply(self) -> str:
        """Read and return the response from the robot."""
        data = b""
        try:
            if self.socket_dobot:
                data = self.socket_dobot.recv(1024)
        except Exception as e:
            logger.error(f"Receive error: {e}")

        data_str = "" if len(data) == 0 else data.decode("utf-8")
        self.log(f"Receive from {self.ip}:{self.port}: {data_str}")
        return data_str

    def sendRecvMsg(self, string: str) -> str:
        """Send a command and wait for response (thread-safe)."""
        with self._global_lock:
            self.send_data(string)
            return self.wait_reply()

    def close(self) -> None:
        """Close the socket connection."""
        if self.socket_dobot:
            logger.info(f"Closing connection to Dobot at {self.ip}:{self.port}")
            self.socket_dobot.close()
            self.socket_dobot = None

    def __del__(self) -> None:
        self.close()

    def __enter__(self) -> DobotApi:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
