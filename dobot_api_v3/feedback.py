"""Feedback interface for Dobot API."""

from __future__ import annotations

import time
from typing import Optional

import numpy as np

from .base import DobotApi, MyType


class DobotApiFeedBack(DobotApi):
    """Feedback interface for reading 1440-byte robot status packets."""

    def __init__(self, ip: str, port: int, *args) -> None:
        super().__init__(ip, port, *args)
        self.__MyType: Optional[np.ndarray] = None
        self.last_recv_time = time.perf_counter()

    def feedBackData(self) -> Optional[np.ndarray]:
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
        self.__MyType = None
        if len(data) == 1440:
            self.__MyType = np.frombuffer(data, dtype=MyType)
        return self.__MyType
