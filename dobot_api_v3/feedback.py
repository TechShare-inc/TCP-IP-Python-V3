"""Feedback interface for Dobot API."""

from __future__ import annotations

import time
from typing import Optional

import numpy as np

from dobot_api_v3.base import DobotApi, FeedbackDtype
from dobot_api_v3.utils import deprecated_alias


class DobotApiFeedback(DobotApi):
    """Feedback interface for reading 1440-byte robot status packets."""

    def __init__(self, ip: str, port: int) -> None:
        """Initialize the feedback socket client.

        Args:
            ip: Robot controller IP address.
            port: Feedback TCP port, usually ``30004``.

        Raises:
            ValueError: If ``port`` is unsupported.
            ConnectionError: If the socket connection fails.
        """
        super().__init__(ip, port)
        self._feedback_dtype: Optional[np.ndarray] = None
        self.last_recv_time = time.perf_counter()

    def feedback_data(self) -> Optional[np.ndarray]:
        """Read one feedback frame and parse it with ``FeedbackDtype``.

        Returns:
            A NumPy structured array of length 1 when a valid 1440-byte frame
            is parsed, otherwise ``None``.

        Raises:
            RuntimeError: If the socket is not connected.
            RuntimeError: If repeated short reads indicate packet loss.
        """
        if self.socket_dobot is None:
            raise RuntimeError(
                "Socket connection is not established. Please connect first."
            )

        self.socket_dobot.setblocking(True)
        temp = self.socket_dobot.recv(144000)

        if len(temp) > 1440:
            temp = self.socket_dobot.recv(144000)

        retries = 0
        if len(temp) < 1440:
            while retries < 5:
                temp = self.socket_dobot.recv(144000)
                if len(temp) > 1440:
                    break
                retries += 1
            if retries >= 5:
                raise RuntimeError(
                    "Missing data packets, please check network environment"
                )

        self.last_recv_time = time.perf_counter()

        data = temp[0:1440]
        self._feedback_dtype = None
        if len(data) == 1440:
            self._feedback_dtype = np.frombuffer(data, dtype=FeedbackDtype)
        return self._feedback_dtype

    @deprecated_alias("feedback_data")
    def feedBackData(self) -> Optional[np.ndarray]:
        """Deprecated alias for :meth:`feedback_data`.

        Returns:
            Same value as :meth:`feedback_data`.
        """
        return self.feedback_data()


# ---------------------------------------------------------------------------
# Deprecated class alias — preserved for backward compatibility.
# PEP 562: module __getattr__ emits DeprecationWarning on access.
# ---------------------------------------------------------------------------
import warnings as _warnings

_DEPRECATED_NAMES: dict[str, object] = {
    "DobotApiFeedBack": DobotApiFeedback,
}


def __getattr__(name: str) -> object:
    """Emit DeprecationWarning for legacy module-level names."""
    if name in _DEPRECATED_NAMES:
        _warnings.warn(
            f"{name} is deprecated, use DobotApiFeedback instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _DEPRECATED_NAMES[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
