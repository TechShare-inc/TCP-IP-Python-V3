"""High-level unified interface for Dobot V3 robots.

``DobotRobot`` is the recommended entry point for new code.  It composes
:class:`~dobot_api_v3.DobotApiDashboard`, :class:`~dobot_api_v3.DobotApiMove`,
:class:`~dobot_api_v3.DobotApiFeedback`, and
:class:`~dobot_api_v3.RobotErrorMonitor` behind a single object so that callers
never have to manage port numbers, multiple ``try/finally`` blocks, or the
``clear_error → power_on → sleep → disable → enable`` startup sequence
themselves.

Example::

    from dobot_api_v3 import DobotRobot

    with DobotRobot("192.168.5.1") as robot:
        robot.startup(speed=40)
        robot.joint_mov_j(-11.53, 4.64, 87.16, -2.84, -77.71, 0.01)
        robot.sync()
        robot.shutdown()
"""

from __future__ import annotations

import time
from typing import Optional

import numpy as np
from loguru import logger

from .base import FeedbackData
from .dashboard import DobotApiDashboard
from .error_monitor import RobotErrorMonitor
from .feedback import DobotApiFeedback
from .move import DobotApiMove
from .utils import DynParam


class DobotRobot:
    """Unified high-level interface for Dobot V3 robots.

    This class manages the dashboard (port 29999) and move (port 30003)
    connections immediately on construction.  Feedback connections on ports
    30004, 30005, and 30006 are created lazily on first access through the
    corresponding properties.

    The individual component objects remain accessible as public attributes
    (``robot.dashboard``, ``robot.move``, etc.) so that the full API surface
    of each subsystem is always reachable.

    Args:
        ip: Robot controller IP address.
        language: Default language for alarm messages (``"en"`` or
            ``"zh_CN"``).

    Example:
        >>> with DobotRobot("192.168.5.1") as robot:
        ...     robot.startup(speed=40)
        ...     robot.mov_j(200, 0, 200, 0, 0, 0)
        ...     robot.sync()
        ...     robot.shutdown()
    """

    def __init__(self, ip: str, *, language: str = "en") -> None:
        """Initialize dashboard and move connections.

        Args:
            ip: Robot controller IP address.
            language: Default alarm language for the error monitor.

        Raises:
            ConnectionError: If any eager socket connection fails.
        """
        self.ip = ip
        self.dashboard: DobotApiDashboard = DobotApiDashboard(ip, 29999)
        self.move: DobotApiMove = DobotApiMove(ip, 30003)
        self.errors: RobotErrorMonitor = RobotErrorMonitor(
            self.dashboard, language=language
        )
        self._feedback: Optional[DobotApiFeedback] = None
        self._feedback_30005: Optional[DobotApiFeedback] = None
        self._feedback_30006: Optional[DobotApiFeedback] = None

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "DobotRobot":
        """Support ``with DobotRobot(...) as robot:`` usage."""
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_val: object,
        exc_tb: object,
    ) -> None:
        """Close all open connections when exiting the ``with`` block."""
        self.close()

    # ------------------------------------------------------------------
    # Lazy feedback properties
    # ------------------------------------------------------------------

    @property
    def feedback(self) -> DobotApiFeedback:
        """Primary feedback connection (port 30004), created on first access.

        Returns:
            A connected :class:`~dobot_api_v3.DobotApiFeedback` instance.
        """
        if self._feedback is None:
            logger.debug(f"Connecting feedback port 30004 on {self.ip}")
            self._feedback = DobotApiFeedback(self.ip, 30004)
        return self._feedback

    @property
    def feedback_30005(self) -> DobotApiFeedback:
        """Secondary feedback connection (port 30005), created on first access.

        Port 30005 provides feedback at a different query frequency than the
        primary port 30004.

        Returns:
            A connected :class:`~dobot_api_v3.DobotApiFeedback` instance.
        """
        if self._feedback_30005 is None:
            logger.debug(f"Connecting feedback port 30005 on {self.ip}")
            self._feedback_30005 = DobotApiFeedback(self.ip, 30005)
        return self._feedback_30005

    @property
    def feedback_30006(self) -> DobotApiFeedback:
        """Tertiary feedback connection (port 30006), created on first access.

        Port 30006 provides feedback at a different query frequency than the
        primary port 30004.

        Returns:
            A connected :class:`~dobot_api_v3.DobotApiFeedback` instance.
        """
        if self._feedback_30006 is None:
            logger.debug(f"Connecting feedback port 30006 on {self.ip}")
            self._feedback_30006 = DobotApiFeedback(self.ip, 30006)
        return self._feedback_30006

    # ------------------------------------------------------------------
    # Lifecycle management
    # ------------------------------------------------------------------

    def startup(
        self,
        speed: int = 40,
        load: float = 0.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
        *,
        power_on_wait: float = 15.0,
    ) -> None:
        """Perform the standard robot startup sequence.

        First checks for controller errors.  If errors are present the
        sequence is ``clear_error → power_on → wait → disable_robot →
        enable_robot → speed_factor``.  If no errors are detected,
        ``clear_error`` and ``power_on`` (and the associated wait) are
        skipped and the sequence continues directly with
        ``disable_robot → enable_robot → speed_factor``.

        Args:
            speed: Global speed factor (1-100) applied after enable.
            load: Payload weight forwarded to :meth:`enable_robot`.
            center_x: Payload center X offset forwarded to
                :meth:`enable_robot`.
            center_y: Payload center Y offset forwarded to
                :meth:`enable_robot`.
            center_z: Payload center Z offset forwarded to
                :meth:`enable_robot`.
            power_on_wait: Seconds to sleep after :meth:`power_on` before
                continuing (default ``15``).  Only used when errors are
                detected and ``power_on`` is called.

        Example:
            >>> robot.startup(speed=50, load=1.0, center_z=0.05)
        """
        logger.info("DobotRobot startup sequence starting")
        has_errors = self.errors.check_errors()
        if has_errors:
            logger.info("Errors detected — clearing and powering on")
            logger.debug(self.dashboard.clear_error())
            logger.debug(self.dashboard.power_on())
            logger.info(f"Waiting {power_on_wait}s for controller to power on")
            time.sleep(power_on_wait)
        else:
            logger.info("No errors detected — skipping clear_error and power_on")
        logger.debug(self.dashboard.disable_robot())
        logger.debug(
            self.dashboard.enable_robot(
                load=load,
                center_x=center_x,
                center_y=center_y,
                center_z=center_z,
            )
        )
        logger.debug(self.dashboard.speed_factor(speed))
        logger.info("DobotRobot startup sequence complete")

    def shutdown(self) -> None:
        """Disable the robot arm (graceful stop).

        Does **not** close TCP connections — call :meth:`close` separately
        when finished, or rely on ``__exit__`` when using as a context manager.

        Example:
            >>> robot.shutdown()
        """
        logger.info("DobotRobot shutdown: disabling robot")
        logger.debug(self.dashboard.disable_robot())

    def close(self) -> None:
        """Close all open TCP connections.

        It is safe to call this method more than once.  Connections that have
        not been opened (e.g. unrequested feedback ports) are silently skipped.

        Example:
            >>> robot.close()
        """
        self.dashboard.close()
        self.move.close()
        if self._feedback is not None:
            self._feedback.close()
            self._feedback = None
        if self._feedback_30005 is not None:
            self._feedback_30005.close()
            self._feedback_30005 = None
        if self._feedback_30006 is not None:
            self._feedback_30006.close()
            self._feedback_30006 = None
        logger.debug("DobotRobot: all connections closed")

    def reconnect(self) -> None:
        """Reconnect all currently-open TCP sockets.

        Opens new sockets for dashboard and move (always), and for whichever
        feedback ports were previously opened.

        Raises:
            ConnectionError: If any reconnection attempt fails.

        Example:
            >>> robot.reconnect()
        """
        self.dashboard.reconnect()
        self.move.reconnect()
        if self._feedback is not None:
            self._feedback.reconnect()
        if self._feedback_30005 is not None:
            self._feedback_30005.reconnect()
        if self._feedback_30006 is not None:
            self._feedback_30006.reconnect()
        logger.info("DobotRobot: all connections reconnected")

    # ------------------------------------------------------------------
    # Error / alarm convenience
    # ------------------------------------------------------------------

    def check_errors(self, language: str = "en") -> bool:
        """Query and log all current alarms.

        Args:
            language: Alarm translation language.

        Returns:
            ``True`` if alarms are present, otherwise ``False``.

        Example:
            >>> has_errors = robot.check_errors(language="en")
        """
        return self.errors.check_errors(language=language)

    def clear_and_recover(self, language: str = "en") -> bool:
        """Display current alarm details then send a clear command.

        Args:
            language: Alarm translation language.

        Returns:
            ``True`` if errors were found and a clear command was sent,
            otherwise ``False``.

        Example:
            >>> robot.clear_and_recover(language="en")
        """
        return self.errors.clear_robot_error(language=language)

    # ------------------------------------------------------------------
    # Feedback convenience
    # ------------------------------------------------------------------

    def feedback_data(self) -> Optional[FeedbackData]:
        """Read one feedback frame from the primary feedback port (30004).

        Opens the feedback connection lazily on the first call.  Returns a
        typed :class:`~dobot_api_v3.FeedbackData` for full IDE autocompletion.
        For zero-copy NumPy access use :meth:`raw_feedback_data` instead.

        Returns:
            A :class:`~dobot_api_v3.FeedbackData` instance when a valid
            1440-byte frame is parsed, otherwise ``None``.

        Example:
            >>> data = robot.feedback_data()
            >>> if data is not None:
            ...     print(data.tool_vector_actual)
            ...     print(data.robot_mode)
        """
        return self.feedback.feedback_data()

    def raw_feedback_data(self) -> Optional[np.ndarray]:
        """Read one feedback frame and return the raw NumPy structured array.

        Opens the feedback connection lazily on the first call.  Use this
        method for NumPy-native numeric pipelines; for typed access prefer
        :meth:`feedback_data`.

        Returns:
            A NumPy structured array of length 1 (``dtype=FeedbackDtype``)
            when a valid 1440-byte frame is parsed, otherwise ``None``.

        Example:
            >>> raw = robot.raw_feedback_data()
            >>> if raw is not None:
            ...     print(raw[0]["tool_vector_actual"])
        """
        return self.feedback.raw_feedback_data()

    # ------------------------------------------------------------------
    # Forwarded dashboard commands
    # ------------------------------------------------------------------

    def enable_robot(
        self,
        load: float = 0.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
    ) -> str:
        """Enable the robot with optional payload parameters.

        Delegates to :meth:`~dobot_api_v3.DobotApiDashboard.enable_robot`.

        Args:
            load: Payload weight.
            center_x: Payload center offset on X axis.
            center_y: Payload center offset on Y axis.
            center_z: Payload center offset on Z axis.

        Returns:
            Robot response string.
        """
        return self.dashboard.enable_robot(
            load=load, center_x=center_x, center_y=center_y, center_z=center_z
        )

    def disable_robot(self) -> str:
        """Disable the robot arm.

        Delegates to :meth:`~dobot_api_v3.DobotApiDashboard.disable_robot`.

        Returns:
            Robot response string.
        """
        return self.dashboard.disable_robot()

    def clear_error(self) -> str:
        """Clear controller alarm information.

        Delegates to :meth:`~dobot_api_v3.DobotApiDashboard.clear_error`.

        Returns:
            Robot response string.
        """
        return self.dashboard.clear_error()

    def reset_robot(self) -> str:
        """Stop the robot.

        Delegates to :meth:`~dobot_api_v3.DobotApiDashboard.reset_robot`.

        Returns:
            Robot response string.
        """
        return self.dashboard.reset_robot()

    def power_on(self) -> str:
        """Power on the controller.

        Delegates to :meth:`~dobot_api_v3.DobotApiDashboard.power_on`.

        Returns:
            Robot response string.
        """
        return self.dashboard.power_on()

    def emergency_stop(self) -> str:
        """Trigger an emergency stop.

        Delegates to :meth:`~dobot_api_v3.DobotApiDashboard.emergency_stop`.

        Returns:
            Robot response string.
        """
        return self.dashboard.emergency_stop()

    def speed_factor(self, speed: int) -> str:
        """Set global speed factor.

        Delegates to :meth:`~dobot_api_v3.DobotApiDashboard.speed_factor`.

        Args:
            speed: Rate value in range 1-100.

        Returns:
            Robot response string.
        """
        return self.dashboard.speed_factor(speed)

    def robot_mode(self) -> str:
        """Query the robot operating mode.

        Delegates to :meth:`~dobot_api_v3.DobotApiDashboard.robot_mode`.

        Returns:
            Robot response string.
        """
        return self.dashboard.robot_mode()

    def get_pose(self) -> str:
        """Get current Cartesian pose.

        Delegates to :meth:`~dobot_api_v3.DobotApiDashboard.get_pose`.

        Returns:
            Robot response string.
        """
        return self.dashboard.get_pose()

    def get_angle(self) -> str:
        """Get current joint angles.

        Delegates to :meth:`~dobot_api_v3.DobotApiDashboard.get_angle`.

        Returns:
            Robot response string.
        """
        return self.dashboard.get_angle()

    def get_error_id(self) -> str:
        """Get current error IDs from the controller.

        Delegates to :meth:`~dobot_api_v3.DobotApiDashboard.get_error_id`.

        Returns:
            Robot response string.
        """
        return self.dashboard.get_error_id()

    def start_drag(self) -> str:
        """Enable drag (teach) mode.

        Delegates to :meth:`~dobot_api_v3.DobotApiDashboard.start_drag`.

        Returns:
            Robot response string.
        """
        return self.dashboard.start_drag()

    def stop_drag(self) -> str:
        """Disable drag (teach) mode.

        Delegates to :meth:`~dobot_api_v3.DobotApiDashboard.stop_drag`.

        Returns:
            Robot response string.
        """
        return self.dashboard.stop_drag()

    def set_user(self, index: int) -> str:
        """Select the calibrated user coordinate system.

        Delegates to :meth:`~dobot_api_v3.DobotApiDashboard.set_user`.

        Args:
            index: Calibrated user coordinate index.

        Returns:
            Robot response string.
        """
        return self.dashboard.set_user(index)

    def set_tool(self, index: int) -> str:
        """Select the calibrated tool coordinate system.

        Delegates to :meth:`~dobot_api_v3.DobotApiDashboard.set_tool`.

        Args:
            index: Calibrated tool coordinate index.

        Returns:
            Robot response string.
        """
        return self.dashboard.set_tool(index)

    # ------------------------------------------------------------------
    # Forwarded move commands
    # ------------------------------------------------------------------

    def mov_j(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
        *dyn_params: DynParam,
    ) -> str:
        """Joint motion interface (point-to-point motion mode).

        Delegates to :meth:`~dobot_api_v3.DobotApiMove.mov_j`.

        Args:
            x: Target X coordinate.
            y: Target Y coordinate.
            z: Target Z coordinate.
            rx: Target RX rotation.
            ry: Target RY rotation.
            rz: Target RZ rotation.
            *dyn_params: Optional motion parameters.

        Returns:
            Robot response string.

        Example:
            >>> robot.mov_j(200, 0, 200, 0, 0, 0)
            >>> robot.mov_j(220, 20, 180, 0, 0, 0, "SpeedJ=40", "AccJ=40")
        """
        return self.move.mov_j(x, y, z, rx, ry, rz, *dyn_params)

    def mov_l(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
        *dyn_params: DynParam,
    ) -> str:
        """Linear motion interface.

        Delegates to :meth:`~dobot_api_v3.DobotApiMove.mov_l`.

        Args:
            x: Target X coordinate.
            y: Target Y coordinate.
            z: Target Z coordinate.
            rx: Target RX rotation.
            ry: Target RY rotation.
            rz: Target RZ rotation.
            *dyn_params: Optional motion parameters.

        Returns:
            Robot response string.

        Example:
            >>> robot.mov_l(250, 0, 180, 0, 0, 0)
        """
        return self.move.mov_l(x, y, z, rx, ry, rz, *dyn_params)

    def joint_mov_j(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        *dyn_params: DynParam,
    ) -> str:
        """Joint motion interface (joint target).

        Delegates to :meth:`~dobot_api_v3.DobotApiMove.joint_mov_j`.

        Args:
            j1: Target joint 1 angle.
            j2: Target joint 2 angle.
            j3: Target joint 3 angle.
            j4: Target joint 4 angle.
            j5: Target joint 5 angle.
            j6: Target joint 6 angle.
            *dyn_params: Optional motion parameters.

        Returns:
            Robot response string.

        Example:
            >>> robot.joint_mov_j(-11.53, 4.64, 87.16, -2.84, -77.71, 0.01)
        """
        return self.move.joint_mov_j(j1, j2, j3, j4, j5, j6, *dyn_params)

    def rel_mov_j(
        self,
        offset1: float,
        offset2: float,
        offset3: float,
        offset4: float,
        offset5: float,
        offset6: float,
        *dyn_params: DynParam,
    ) -> str:
        """Relative joint offset motion (point-to-point mode).

        Delegates to :meth:`~dobot_api_v3.DobotApiMove.rel_mov_j`.

        Args:
            offset1: Joint 1 offset.
            offset2: Joint 2 offset.
            offset3: Joint 3 offset.
            offset4: Joint 4 offset.
            offset5: Joint 5 offset.
            offset6: Joint 6 offset.
            *dyn_params: Optional motion parameters.

        Returns:
            Robot response string.

        Example:
            >>> robot.rel_mov_j(15, 0, 0, 0, 0, 0)
        """
        return self.move.rel_mov_j(
            offset1, offset2, offset3, offset4, offset5, offset6, *dyn_params
        )

    def rel_mov_l(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        *dyn_params: DynParam,
    ) -> str:
        """Relative Cartesian offset motion (linear mode).

        Delegates to :meth:`~dobot_api_v3.DobotApiMove.rel_mov_l`.

        Args:
            offset_x: X-axis offset.
            offset_y: Y-axis offset.
            offset_z: Z-axis offset.
            *dyn_params: Optional motion parameters.

        Returns:
            Robot response string.
        """
        return self.move.rel_mov_l(offset_x, offset_y, offset_z, *dyn_params)

    def arc(
        self,
        x1: float,
        y1: float,
        z1: float,
        a1: float,
        b1: float,
        c1: float,
        x2: float,
        y2: float,
        z2: float,
        a2: float,
        b2: float,
        c2: float,
        *dyn_params: DynParam,
    ) -> str:
        """Circular motion through an intermediate point.

        Delegates to :meth:`~dobot_api_v3.DobotApiMove.arc`.

        Args:
            x1: Intermediate point X.
            y1: Intermediate point Y.
            z1: Intermediate point Z.
            a1: Intermediate point A.
            b1: Intermediate point B.
            c1: Intermediate point C.
            x2: End point X.
            y2: End point Y.
            z2: End point Z.
            a2: End point A.
            b2: End point B.
            c2: End point C.
            *dyn_params: Optional motion parameters.

        Returns:
            Robot response string.
        """
        return self.move.arc(
            x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, *dyn_params
        )

    def servo_j(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        t: float = 0.1,
        lookahead_time: float = 50.0,
        gain: float = 500.0,
    ) -> str:
        """Dynamic following in joint space.

        Delegates to :meth:`~dobot_api_v3.DobotApiMove.servo_j`.

        Args:
            j1: Target joint 1 angle.
            j2: Target joint 2 angle.
            j3: Target joint 3 angle.
            j4: Target joint 4 angle.
            j5: Target joint 5 angle.
            j6: Target joint 6 angle.
            t: Point run time in seconds.
            lookahead_time: Feed-forward smoothing parameter.
            gain: Servo gain parameter.

        Returns:
            Robot response string.
        """
        return self.move.servo_j(j1, j2, j3, j4, j5, j6, t, lookahead_time, gain)

    def servo_p(
        self,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
    ) -> str:
        """Dynamic following in Cartesian space.

        Delegates to :meth:`~dobot_api_v3.DobotApiMove.servo_p`.

        Args:
            x: Target X coordinate.
            y: Target Y coordinate.
            z: Target Z coordinate.
            a: Target A rotation.
            b: Target B rotation.
            c: Target C rotation.

        Returns:
            Robot response string.
        """
        return self.move.servo_p(x, y, z, a, b, c)

    def move_jog(self, axis_id: str, *dyn_params: DynParam) -> str:
        """Jog motion along a single axis.

        Delegates to :meth:`~dobot_api_v3.DobotApiMove.move_jog`.

        Args:
            axis_id: Axis command such as ``"J1+"`` or ``"X-"``.
            *dyn_params: Optional jog parameters ``(coord_type, user, tool)``.

        Returns:
            Robot response string.

        Example:
            >>> robot.move_jog("J1+")
            >>> robot.move_jog("")  # stop jog
        """
        return self.move.move_jog(axis_id, *dyn_params)

    def sync(self) -> str:
        """Block until all queued motion commands complete.

        Delegates to :meth:`~dobot_api_v3.DobotApiMove.sync`.

        Returns:
            Robot response string.

        Example:
            >>> robot.mov_j(200, 0, 200, 0, 0, 0)
            >>> robot.sync()
        """
        return self.move.sync()

    def __repr__(self) -> str:
        return f"DobotRobot(ip={self.ip!r})"
