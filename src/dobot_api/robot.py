"""Unified V3/V4 Dobot robot facade."""

from __future__ import annotations

import time
import warnings
from typing import Literal, Optional

import numpy as np

from .dtypes import FeedbackData
from .error_monitor import RobotErrorMonitor
from .feedback import DobotApiFeedback


Protocol = Literal["v3", "v4"]


class DobotRobot:
    """Single public entry point for Dobot V3 and V4 TCP protocols."""

    def __init__(self, ip: str, protocol: Protocol, *, language: str = "en") -> None:
        self.ip = ip
        self.protocol = protocol
        self._language = language

        if protocol == "v3":
            from .v3 import DobotApiDashboard, DobotApiMove

            self.dashboard = DobotApiDashboard(ip, 29999)
            self._motion_backend = DobotApiMove(ip, 30003)
        elif protocol == "v4":
            from .v4 import DobotApiDashboard

            self.dashboard = DobotApiDashboard(ip, 29999)
            self._motion_backend = self.dashboard
        else:
            raise ValueError(f"Unknown protocol: {protocol}")

        self.errors = RobotErrorMonitor(
            self.dashboard,
            protocol=protocol,
        )
        self._feedback: Optional[DobotApiFeedback] = None
        self._feedback_30005: Optional[DobotApiFeedback] = None
        self._feedback_30006: Optional[DobotApiFeedback] = None

    @property
    def move(self):
        """Deprecated compatibility alias for the active motion backend."""
        warnings.warn(
            "DobotRobot.move is deprecated; call motion methods on DobotRobot directly.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._motion_backend

    @property
    def feedback(self) -> DobotApiFeedback:
        if self._feedback is None:
            self._feedback = DobotApiFeedback(self.ip, 30004, protocol=self.protocol)
        return self._feedback

    @property
    def feedback_30005(self) -> DobotApiFeedback:
        if self._feedback_30005 is None:
            self._feedback_30005 = DobotApiFeedback(self.ip, 30005, protocol=self.protocol)
        return self._feedback_30005

    @property
    def feedback_30006(self) -> DobotApiFeedback:
        if self._feedback_30006 is None:
            self._feedback_30006 = DobotApiFeedback(self.ip, 30006, protocol=self.protocol)
        return self._feedback_30006

    def close(self) -> None:
        self.dashboard.close()
        if self._motion_backend is not self.dashboard:
            self._motion_backend.close()
        for attr in ("_feedback", "_feedback_30005", "_feedback_30006"):
            feedback = getattr(self, attr)
            if feedback is not None:
                feedback.close()
                setattr(self, attr, None)

    def reconnect(self) -> None:
        self.dashboard.reconnect()
        if self._motion_backend is not self.dashboard:
            self._motion_backend.reconnect()
        for feedback in (self._feedback, self._feedback_30005, self._feedback_30006):
            if feedback is not None:
                feedback.reconnect()

    def __enter__(self) -> "DobotRobot":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def startup(
        self,
        speed: int = 40,
        load: float = 0.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
        *,
        power_on_wait: float = 20.0,
    ) -> None:
        self.clear_error()
        if self.protocol == "v3":
            self.power_on()
            time.sleep(power_on_wait)
            self.disable_robot()
        self.enable_robot(load, center_x, center_y, center_z)
        self.speed_factor(speed)

    def shutdown(self) -> None:
        self.disable_robot()

    def check_errors(self, language: str = "en") -> bool:
        return self.errors.check_errors(language=language)

    def clear_robot_error(self, language: str = "en") -> bool:
        return self.errors.clear_robot_error(language=language)

    def feedback_data(self) -> Optional[FeedbackData]:
        return self.feedback.feedback_data()

    def raw_feedback_data(self) -> Optional[np.ndarray]:
        return self.feedback.raw_feedback_data()

    def speed_j(self, *args, **kwargs):
        warnings.warn("speed_j() is deprecated; use vel_j().", DeprecationWarning, stacklevel=2)
        return self.vel_j(*args, **kwargs)

    def speed_l(self, *args, **kwargs):
        warnings.warn("speed_l() is deprecated; use vel_l().", DeprecationWarning, stacklevel=2)
        return self.vel_l(*args, **kwargs)

    def vel_j(self, *args, **kwargs):
        backend = self.dashboard
        if hasattr(backend, "vel_j"):
            return backend.vel_j(*args, **kwargs)
        return backend.speed_j(*args, **kwargs)

    def vel_l(self, *args, **kwargs):
        backend = self.dashboard
        if hasattr(backend, "vel_l"):
            return backend.vel_l(*args, **kwargs)
        return backend.speed_l(*args, **kwargs)

    def mov_j(self, a1, b1, c1, d1, e1, f1, coordinate_mode=0, *args, **kwargs):
        if self.protocol == "v3" and coordinate_mode == 1:
            return self._motion_backend.joint_mov_j(a1, b1, c1, d1, e1, f1, *args, **kwargs)
        if self.protocol == "v3":
            return self._motion_backend.mov_j(a1, b1, c1, d1, e1, f1, *args, **kwargs)
        return self._motion_backend.mov_j(a1, b1, c1, d1, e1, f1, coordinate_mode, *args, **kwargs)

    def mov_l(self, a1, b1, c1, d1, e1, f1, coordinate_mode=0, *args, **kwargs):
        if self.protocol == "v3":
            return self._motion_backend.mov_l(a1, b1, c1, d1, e1, f1, *args, **kwargs)
        return self._motion_backend.mov_l(a1, b1, c1, d1, e1, f1, coordinate_mode, *args, **kwargs)

    def rel_mov_j(self, *args, **kwargs):
        if self.protocol == "v4":
            raise NotImplementedError("rel_mov_j is not available on V4 protocol")
        return self._motion_backend.rel_mov_j(*args, **kwargs)

    def joint_mov_j(self, *args, **kwargs):
        if self.protocol == "v4":
            return self.mov_j(*args, coordinate_mode=1, **kwargs)
        return self._motion_backend.joint_mov_j(*args, **kwargs)

    def servo_js(self, *args, **kwargs):
        if not hasattr(self._motion_backend, "servo_js"):
            return self._motion_backend.servo_j(*args, **kwargs)
        return self._motion_backend.servo_js(*args, **kwargs)

    def __getattr__(self, name: str):
        if hasattr(self.dashboard, name):
            return getattr(self.dashboard, name)
        if hasattr(self._motion_backend, name):
            return getattr(self._motion_backend, name)
        raise AttributeError(name)

    def __repr__(self) -> str:
        return f"DobotRobot(ip={self.ip!r}, protocol={self.protocol!r})"
