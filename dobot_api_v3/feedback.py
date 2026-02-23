"""Feedback interface for Dobot API."""

from __future__ import annotations

import time
from typing import Optional

import numpy as np

from dobot_api_v3.base import DobotApi, FeedbackData, FeedbackDtype
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

    def raw_feedback_data(self) -> Optional[np.ndarray]:
        """Read one feedback frame and return the raw NumPy structured array.

        Use this method when you need zero-copy NumPy access to the packet
        fields (e.g., for numeric pipelines or direct array slicing).  For
        typed, IDE-friendly access prefer :meth:`feedback_data` instead.

        Returns:
            A NumPy structured array of length 1 (``dtype=FeedbackDtype``)
            when a valid 1440-byte frame is parsed, otherwise ``None``.

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

    def feedback_data(self) -> Optional[FeedbackData]:
        """Read one feedback frame and return a typed :class:`~dobot_api_v3.FeedbackData`.

        Internally calls :meth:`raw_feedback_data` and converts the result to
        an immutable :class:`~dobot_api_v3.FeedbackData` dataclass for full
        IDE autocompletion and type-checker support.

        For zero-copy NumPy access (e.g., numeric pipelines) use
        :meth:`raw_feedback_data` directly.

        Returns:
            A :class:`~dobot_api_v3.FeedbackData` instance when a valid
            1440-byte frame is parsed, otherwise ``None``.

        Raises:
            RuntimeError: If the socket is not connected.
            RuntimeError: If repeated short reads indicate packet loss.

        Example:
            >>> data = feedback.feedback_data()
            >>> if data is not None:
            ...     print(data.robot_mode)
            ...     print(data.tool_vector_actual)
        """
        raw = self.raw_feedback_data()
        if raw is None:
            return None
        return FeedbackData.from_numpy(raw)

    @deprecated_alias("feedback_data")
    def feedBackData(self) -> Optional[FeedbackData]:
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
