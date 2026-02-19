"""Feedback interface for Dobot API."""

from __future__ import annotations

import time
from typing import Optional

import numpy as np

from .base import DobotApi, FeedbackDtype
from .utils import deprecated_alias


class DobotApiFeedback(DobotApi):
    """Feedback interface for reading 1440-byte robot status packets."""

    def __init__(self, ip: str, port: int) -> None:
        super().__init__(ip, port)
        self._feedback_dtype: Optional[np.ndarray] = None
        self.last_recv_time = time.perf_counter()

    def feedback_data(self) -> Optional[np.ndarray]:
        """Read one 1440-byte robot status packet and return it as a numpy array."""
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
        """Deprecated — use :meth:`feedback_data` instead."""
        return self.feedback_data()


# ---------------------------------------------------------------------------
# Deprecated class alias — preserved for backward compatibility.
# ---------------------------------------------------------------------------
DobotApiFeedBack = DobotApiFeedback  # deprecated: use DobotApiFeedback
