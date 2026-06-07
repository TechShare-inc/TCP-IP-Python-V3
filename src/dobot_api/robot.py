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

    # ------------------------------------------------------------------
    # Additional explicit motion stubs (design: one-liner bodies)
    # ------------------------------------------------------------------

    def servo_j(self, j1, j2, j3, j4, j5, j6, t=0.1, ahead_time=50.0, gain=500.0, **kwargs):
        """Servo to joint angles (streaming)."""
        return self._motion_backend.servo_j(j1, j2, j3, j4, j5, j6, t, ahead_time, gain, **kwargs)

    def servo_p(self, x, y, z, rx, ry, rz, t=0.1, ahead_time=50.0, gain=500.0, **kwargs):
        """Servo to Cartesian pose (streaming)."""
        return self._motion_backend.servo_p(x, y, z, rx, ry, rz, t, ahead_time, gain, **kwargs)

    def arc(self, a1, b1, c1, d1, e1, f1, a2, b2, c2, d2, e2, f2, *args, **kwargs):
        """Arc motion through a via-point."""
        return self._motion_backend.arc(
            a1, b1, c1, d1, e1, f1, a2, b2, c2, d2, e2, f2, *args, **kwargs
        )

    def move_jog(self, axis_id="", *args, **kwargs):
        """Start or update a jog motion."""
        return self._motion_backend.move_jog(axis_id, *args, **kwargs)

    def circle(self, a1, b1, c1, d1, e1, f1, a2, b2, c2, d2, e2, f2, count, *args, **kwargs):
        """Circle motion."""
        if self.protocol == "v3":
            raise NotImplementedError("circle is not available on V3 protocol")
        return self._motion_backend.circle(
            a1, b1, c1, d1, e1, f1, a2, b2, c2, d2, e2, f2, count, *args, **kwargs
        )

    # ------------------------------------------------------------------
    # V3-only motion commands (NotImplementedError on V4)
    # ------------------------------------------------------------------

    def rel_mov_l(self, offset_x, offset_y, offset_z, *args, **kwargs):
        """Relative linear motion (V3 only)."""
        if self.protocol == "v4":
            raise NotImplementedError("rel_mov_l is not available on V4 protocol")
        return self._motion_backend.rel_mov_l(offset_x, offset_y, offset_z, *args, **kwargs)

    def rel_mov_j_tool(self, *args, **kwargs):
        """Relative joint motion in tool frame (V3 only)."""
        if self.protocol == "v4":
            raise NotImplementedError("rel_mov_j_tool is not available on V4 protocol")
        return self._motion_backend.rel_mov_j_tool(*args, **kwargs)

    def rel_mov_l_tool(self, *args, **kwargs):
        """Relative linear motion in tool frame (V3 only)."""
        if self.protocol == "v4":
            raise NotImplementedError("rel_mov_l_tool is not available on V4 protocol")
        return self._motion_backend.rel_mov_l_tool(*args, **kwargs)

    def rel_mov_j_user(self, *args, **kwargs):
        """Relative joint motion in user frame (V3 only)."""
        if self.protocol == "v4":
            raise NotImplementedError("rel_mov_j_user is not available on V4 protocol")
        return self._motion_backend.rel_mov_j_user(*args, **kwargs)

    def rel_mov_l_user(self, *args, **kwargs):
        """Relative linear motion in user frame (V3 only)."""
        if self.protocol == "v4":
            raise NotImplementedError("rel_mov_l_user is not available on V4 protocol")
        return self._motion_backend.rel_mov_l_user(*args, **kwargs)

    def rel_joint_mov_j(self, *args, **kwargs):
        """Relative joint-space motion (V3 only)."""
        if self.protocol == "v4":
            raise NotImplementedError("rel_joint_mov_j is not available on V4 protocol")
        return self._motion_backend.rel_joint_mov_j(*args, **kwargs)

    def sync(self, *args, **kwargs):
        """Wait for motion queue to drain (V3 only)."""
        if self.protocol == "v4":
            raise NotImplementedError("sync is not available on V4 protocol")
        return self._motion_backend.sync(*args, **kwargs)

    def start_trace(self, *args, **kwargs):
        """Start trajectory replay (V3 only)."""
        if self.protocol == "v4":
            raise NotImplementedError("start_trace is not available on V4 protocol")
        return self._motion_backend.start_trace(*args, **kwargs)

    def start_path(self, *args, **kwargs):
        """Start path replay (V3 only)."""
        if self.protocol == "v4":
            raise NotImplementedError("start_path is not available on V4 protocol")
        return self._motion_backend.start_path(*args, **kwargs)

    def start_fc_trace(self, *args, **kwargs):
        """Start force-controlled trace (V3 only)."""
        if self.protocol == "v4":
            raise NotImplementedError("start_fc_trace is not available on V4 protocol")
        return self._motion_backend.start_fc_trace(*args, **kwargs)

    # ------------------------------------------------------------------
    # V3-only dashboard commands (NotImplementedError on V4)
    # ------------------------------------------------------------------

    def arch(self, *args, **kwargs):
        """Set arch index (V3 only)."""
        if self.protocol == "v4":
            raise NotImplementedError("arch is not available on V4 protocol")
        return self.dashboard.arch(*args, **kwargs)

    def lim_z(self, *args, **kwargs):
        """Set Z limit (V3 only)."""
        if self.protocol == "v4":
            raise NotImplementedError("lim_z is not available on V4 protocol")
        return self.dashboard.lim_z(*args, **kwargs)

    def set_arm_orientation(self, *args, **kwargs):
        """Set arm orientation (V3 only)."""
        if self.protocol == "v4":
            raise NotImplementedError("set_arm_orientation is not available on V4 protocol")
        return self.dashboard.set_arm_orientation(*args, **kwargs)

    def pause(self, *args, **kwargs):
        """Pause execution (V3 only; V4 uses pause_script)."""
        if self.protocol == "v4":
            raise NotImplementedError("pause is not available on V4 protocol; use pause_script")
        return self.dashboard.pause(*args, **kwargs)

    def resume(self, *args, **kwargs):
        """Resume execution (V3 only)."""
        if self.protocol == "v4":
            raise NotImplementedError("resume is not available on V4 protocol")
        return self.dashboard.resume(*args, **kwargs)

    def wait(self, *args, **kwargs):
        """Wait for a duration in seconds (V3 only; V4 uses sleep)."""
        if self.protocol == "v4":
            raise NotImplementedError("wait is not available on V4 protocol; use sleep")
        return self.dashboard.wait(*args, **kwargs)

    # ------------------------------------------------------------------
    # V4-only motion commands (NotImplementedError on V3)
    # ------------------------------------------------------------------

    def mov_j_io(self, *args, **kwargs):
        """Joint motion with I/O trigger (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("mov_j_io is not available on V3 protocol")
        return self._motion_backend.mov_j_io(*args, **kwargs)

    def mov_l_io(self, *args, **kwargs):
        """Linear motion with I/O trigger (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("mov_l_io is not available on V3 protocol")
        return self._motion_backend.mov_l_io(*args, **kwargs)

    def arc_io(self, *args, **kwargs):
        """Arc motion with I/O trigger (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("arc_io is not available on V3 protocol")
        return self._motion_backend.arc_io(*args, **kwargs)

    # ------------------------------------------------------------------
    # V4-only force-compliance commands (NotImplementedError on V3)
    # ------------------------------------------------------------------

    def fc_force_mode(self, *args, **kwargs):
        """Enable force compliance mode (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("fc_force_mode is not available on V3 protocol")
        return self.dashboard.fc_force_mode(*args, **kwargs)

    def fc_off(self, *args, **kwargs):
        """Disable force compliance (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("fc_off is not available on V3 protocol")
        return self.dashboard.fc_off(*args, **kwargs)

    def fc_set_deviation(self, *args, **kwargs):
        """Set force deviation (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("fc_set_deviation is not available on V3 protocol")
        return self.dashboard.fc_set_deviation(*args, **kwargs)

    def fc_set_force_limit(self, *args, **kwargs):
        """Set force limit (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("fc_set_force_limit is not available on V3 protocol")
        return self.dashboard.fc_set_force_limit(*args, **kwargs)

    def fc_set_mass(self, *args, **kwargs):
        """Set mass parameter (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("fc_set_mass is not available on V3 protocol")
        return self.dashboard.fc_set_mass(*args, **kwargs)

    def fc_set_stiffness(self, *args, **kwargs):
        """Set stiffness parameter (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("fc_set_stiffness is not available on V3 protocol")
        return self.dashboard.fc_set_stiffness(*args, **kwargs)

    def fc_set_damping(self, *args, **kwargs):
        """Set damping parameter (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("fc_set_damping is not available on V3 protocol")
        return self.dashboard.fc_set_damping(*args, **kwargs)

    def enable_ft_sensor(self, *args, **kwargs):
        """Enable force/torque sensor (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("enable_ft_sensor is not available on V3 protocol")
        return self.dashboard.enable_ft_sensor(*args, **kwargs)

    def force_drive_mode(self, *args, **kwargs):
        """Set force drive mode (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("force_drive_mode is not available on V3 protocol")
        return self.dashboard.force_drive_mode(*args, **kwargs)

    # ------------------------------------------------------------------
    # V4-only conveyor commands (NotImplementedError on V3)
    # ------------------------------------------------------------------

    def cnv_init(self, *args, **kwargs):
        """Initialise conveyor tracking (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("cnv_init is not available on V3 protocol")
        return self.dashboard.cnv_init(*args, **kwargs)

    def cnv_mov_l(self, *args, **kwargs):
        """Conveyor-tracked linear motion (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("cnv_mov_l is not available on V3 protocol")
        return self.dashboard.cnv_mov_l(*args, **kwargs)

    # ------------------------------------------------------------------
    # V4-only weld commands (NotImplementedError on V3)
    # ------------------------------------------------------------------

    def arc_track_start(self, *args, **kwargs):
        """Start arc tracking (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("arc_track_start is not available on V3 protocol")
        return self.dashboard.arc_track_start(*args, **kwargs)

    def arc_track_end(self, *args, **kwargs):
        """End arc tracking (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("arc_track_end is not available on V3 protocol")
        return self.dashboard.arc_track_end(*args, **kwargs)

    def weave_start(self, *args, **kwargs):
        """Start weave welding (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("weave_start is not available on V3 protocol")
        return self.dashboard.weave_start(*args, **kwargs)

    # ------------------------------------------------------------------
    # V4-only check commands (NotImplementedError on V3)
    # ------------------------------------------------------------------

    def check_mov_j(self, *args, **kwargs):
        """Pre-check joint motion reachability (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("check_mov_j is not available on V3 protocol")
        return self.dashboard.check_mov_j(*args, **kwargs)

    def check_mov_l(self, *args, **kwargs):
        """Pre-check linear motion reachability (V4 only)."""
        if self.protocol == "v3":
            raise NotImplementedError("check_mov_l is not available on V3 protocol")
        return self.dashboard.check_mov_l(*args, **kwargs)

    # ------------------------------------------------------------------
    # Fallback: route unknown methods to dashboard, then motion backend
    # ------------------------------------------------------------------

    def __getattr__(self, name: str):
        if hasattr(self.dashboard, name):
            return getattr(self.dashboard, name)
        if hasattr(self._motion_backend, name):
            return getattr(self._motion_backend, name)
        raise AttributeError(
            f"{type(self).__name__!r} object has no attribute {name!r}"
        )

    def __repr__(self) -> str:
        return f"DobotRobot(ip={self.ip!r}, protocol={self.protocol!r})"
