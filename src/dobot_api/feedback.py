"""Protocol-aware feedback reader."""

from __future__ import annotations

from typing import Literal, Optional

import numpy as np

from .dtypes import FeedbackData


class DobotApiFeedback:
    """Feedback facade that normalizes V3 and V4 feedback packets."""

    def __init__(
        self,
        ip: str,
        port: int,
        *,
        protocol: Literal["v3", "v4"],
    ) -> None:
        self.protocol = protocol
        if protocol == "v3":
            from .v3 import DobotApiFeedback as BackendFeedback
        elif protocol == "v4":
            from .v4 import DobotApiFeedback as BackendFeedback
        else:
            raise ValueError(f"Unknown protocol: {protocol}")
        self._backend = BackendFeedback(ip, port)

    @property
    def port(self) -> int:
        return int(self._backend.port)

    @property
    def socket_dobot(self):
        return self._backend.socket_dobot

    def raw_feedback_data(self) -> Optional[np.ndarray]:
        return self._backend.raw_feedback_data()

    def feedback_data(self) -> Optional[FeedbackData]:
        raw = self.raw_feedback_data()
        if raw is None:
            return None
        return FeedbackData.from_numpy(raw)

    def close(self) -> None:
        self._backend.close()

    def reconnect(self) -> None:
        self._backend.reconnect()
