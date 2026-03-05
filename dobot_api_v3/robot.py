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

The forwarded command methods (everything below the ``# --- BEGIN
AUTO-GENERATED ---`` marker) are produced by ``dobot_api_v3/_codegen.py``.
Re-run the generator after adding commands to a mixin::

    uv run python -m dobot_api_v3._codegen
"""

from __future__ import annotations

import time
from typing import Optional

import numpy as np
from loguru import logger

from .dtypes import FeedbackData
from .commands.dashboard import DobotApiDashboard
from .commands.move import DobotApiMove
from .error_monitor import RobotErrorMonitor
from .feedback import DobotApiFeedback
from .utils import DynParam, Pose, ToolDynParam


class DobotRobot:
    """Unified high-level interface for Dobot V3 robots.

    This class manages the dashboard (port 29999) and move (port 30003)
    connections immediately on construction.  Feedback connections on ports
    30004, 30005, and 30006 are created lazily on first access through the
    corresponding properties.

    The individual component objects remain accessible as public attributes
    (``robot.dashboard``, ``robot.move``, etc.) so that the full API surface
    of each subsystem is always reachable.

    All public methods of :class:`~dobot_api_v3.DobotApiDashboard` and
    :class:`~dobot_api_v3.DobotApiMove` are mirrored directly on this class
    as one-liner forwarding methods so users never need to reach through
    ``robot.dashboard`` or ``robot.move`` for day-to-day use.

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
        power_on_wait: float = 20.0,
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
            logger.debug(self.clear_error())
            logger.debug(self.power_on())
            logger.info(f"Waiting {power_on_wait}s for controller to power on")
            time.sleep(power_on_wait)
        else:
            logger.info("No errors detected — skipping clear_error and power_on")
        logger.debug(self.disable_robot())
        logger.debug(
            self.enable_robot(
                load=load,
                center_x=center_x,
                center_y=center_y,
                center_z=center_z,
            )
        )
        logger.debug(self.speed_factor(speed))
        logger.info("DobotRobot startup sequence complete")

    def shutdown(self) -> None:
        """Disable the robot arm (graceful stop).

        Does **not** close TCP connections — call :meth:`close` separately
        when finished, or rely on ``__exit__`` when using as a context manager.

        Example:
            >>> robot.shutdown()
        """
        logger.info("DobotRobot shutdown: disabling robot")
        logger.debug(self.disable_robot())

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
    # Forwarded dashboard and move commands
    # (auto-generated — do not edit by hand; run _codegen.py to refresh)
    # ------------------------------------------------------------------

    # --- BEGIN AUTO-GENERATED ---
    # -- dashboard --------------------------------------------------------
    def acc_j(self, speed: int) -> int:
        """Set joint acceleration ratio (MovJ / MovJIO / MovJR / JointMovJ).

        Args:
            speed: Joint acceleration ratio (1-100).

        Returns:
            Command queue ID.
        """
        return self.dashboard.acc_j(speed)

    def acc_l(self, speed: int) -> int:
        """Set Cartesian acceleration ratio (MovL / MovLIO / MovLR / Jump / Arc / Circle).

        Args:
            speed: Cartesian acceleration ratio (1-100).

        Returns:
            Command queue ID.
        """
        return self.dashboard.acc_l(speed)

    def ao(self, index: int, val: float) -> int:
        """Set analog signal output (queued).

        Args:
            index: Analog output index (1-2).
            val: Output voltage (0-10).

        Returns:
            Command queue ID.
        """
        return self.dashboard.ao(index, val)

    def ao_execute(self, index: int, val: float) -> int:
        """Set analog signal output (immediate).

        Args:
            index: Analog output index (1-2).
            val: Output voltage (0-10).

        Returns:
            Command queue ID.
        """
        return self.dashboard.ao_execute(index, val)

    def arch(self, index: int) -> int:
        """Set Jump gate parameter index (start lift height, max lift, end drop).

        Args:
            index: Jump parameter index (0-9).

        Returns:
            Command queue ID.
        """
        return self.dashboard.arch(index)

    def brake_control(self, offset1: int, offset2: int) -> int:
        """Control joint brakes.

        Args:
            offset1: Joint index.
            offset2: Brake control value.

        Returns:
            Command queue ID.
        """
        return self.dashboard.brake_control(offset1, offset2)

    def clear_error(self) -> int:
        """Clear controller alarm information.

        Returns:
            Command queue ID.

        Example:
            >>> dashboard.clear_error()
        """
        return self.dashboard.clear_error()

    def continue_script(self) -> int:
        """Continue running the script.

        Returns:
            Command queue ID.
        """
        return self.dashboard.continue_script()

    def cp(self, ratio: int) -> int:
        """Set smooth transition ratio.

        Args:
            ratio: Smooth transition ratio (1-100).

        Returns:
            Command queue ID.
        """
        return self.dashboard.cp(ratio)

    def di(self, offset1: int) -> int:
        """Read a digital input port.

        Args:
            offset1: Digital input index.

        Returns:
            Digital input state (0 or 1).
        """
        return self.dashboard.di(offset1)

    def disable_robot(self) -> int:
        """Disable the robot arm.

        Returns:
            Command queue ID.
        """
        return self.dashboard.disable_robot()

    def do_execute(self, index: int, status: int) -> int:
        """Set digital signal output (immediate).

        Args:
            index: Digital output index (1-24).
            status: Output state (0 for low, 1 for high).

        Returns:
            Command queue ID.
        """
        return self.dashboard.do_execute(index, status)

    def do_group(self, *dyn_params: DynParam) -> int:
        """Set multiple digital outputs in one command.

        Args:
            *dyn_params: Repeating output pairs such as ``(index, status)``.

        Returns:
            Command queue ID.
        """
        return self.dashboard.do_group(*dyn_params)

    def do_output(self, index: int, status: int) -> int:
        """Set digital signal output (queued).

        Args:
            index: Digital output index (1-24).
            status: Output state (0 for low, 1 for high).

        Returns:
            Command queue ID.
        """
        return self.dashboard.do_output(index, status)

    def emergency_stop(self) -> int:
        """Trigger emergency stop.

        Returns:
            Command queue ID.
        """
        return self.dashboard.emergency_stop()

    def enable_robot(self, load: float = 0.0, center_x: float = 0.0, center_y: float = 0.0, center_z: float = 0.0) -> int:
        """Enable the robot with optional payload parameters.

        Args:
            load: Payload weight.
            center_x: Payload center offset on X axis.
            center_y: Payload center offset on Y axis.
            center_z: Payload center offset on Z axis.

        Returns:
            Command queue ID.

        Example:
            >>> dashboard.enable_robot()
            >>> dashboard.enable_robot(load=0.5, center_x=0.0, center_y=0.0, center_z=0.05)
        """
        return self.dashboard.enable_robot(load, center_x, center_y, center_z)

    def get_angle(self) -> Pose:
        """Get current joint angles.

        Returns:
            Joint angles as ``(j1, j2, j3, j4, j5, j6)``.
        """
        return self.dashboard.get_angle()

    def get_coils(self, offset1: int, offset2: int, offset3: int) -> tuple[int, ...]:
        """Read coil values.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Coil count.

        Returns:
            Tuple of coil values as integers.
        """
        return self.dashboard.get_coils(offset1, offset2, offset3)

    def get_error_id(self) -> tuple[int, ...]:
        """Get robot error code.

        Returns:
            Tuple of non-zero alarm codes (may be empty).
        """
        return self.dashboard.get_error_id()

    def get_hold_regs(self, id: int, addr: int, count: int, type_: str) -> tuple[float, ...]:
        """Read hold register.

        Args:
            id: Secondary device number (0-4, where 0 is controller slave).
            addr: Starting hold-register address (3095-4095).
            count: Number of items to read (1-16).
            type_: Data type, such as ``"U16"``, ``"U32"``, ``"F32"``, or
                ``"F64"``.

        Returns:
            Tuple of register values as floats.
        """
        return self.dashboard.get_hold_regs(id, addr, count, type_)

    def get_in_bits(self, offset1: int, offset2: int, offset3: int) -> tuple[int, ...]:
        """Read digital input bits.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Number of bits.

        Returns:
            Tuple of bit values as integers.
        """
        return self.dashboard.get_in_bits(offset1, offset2, offset3)

    def get_in_regs(self, offset1: int, offset2: int, offset3: int, *dyn_params: DynParam) -> tuple[float, ...]:
        """Read input registers.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Register count.
            *dyn_params: Optional data type and mode parameters.

        Returns:
            Tuple of register values as floats.
        """
        return self.dashboard.get_in_regs(offset1, offset2, offset3, *dyn_params)

    def get_path_start_pose(self, offset1: str) -> Pose:
        """Get starting pose of a joint path file.

        Args:
            offset1: Path file name.

        Returns:
            Starting pose as ``(x, y, z, rx, ry, rz)``.
        """
        return self.dashboard.get_path_start_pose(offset1)

    def get_pose(self) -> Pose:
        """Get current Cartesian pose.

        Returns:
            Cartesian pose as ``(x, y, z, rx, ry, rz)``.
        """
        return self.dashboard.get_pose()

    def get_six_force_data(self) -> Pose:
        """Read six-axis force sensor data.

        Returns:
            Force/torque values as ``(fx, fy, fz, mx, my, mz)``.
        """
        return self.dashboard.get_six_force_data()

    def get_terminal_485(self) -> tuple[str, ...]:
        """Get terminal RS-485 configuration.

        Returns:
            Tuple of configuration tokens (baud, data bits, parity, stop bits).
        """
        return self.dashboard.get_terminal_485()

    def get_trace_start_pose(self, offset1: str) -> Pose:
        """Get starting pose of a Cartesian trajectory file.

        Args:
            offset1: Trajectory file name.

        Returns:
            Starting pose as ``(x, y, z, rx, ry, rz)``.
        """
        return self.dashboard.get_trace_start_pose(offset1)

    def handle_traj_points(self, offset1: str) -> int:
        """Process a trajectory points file.

        Args:
            offset1: Trajectory file name.

        Returns:
            Command queue ID.
        """
        return self.dashboard.handle_traj_points(offset1)

    def inverse_solution(self, offset1: float, offset2: float, offset3: float, offset4: float, offset5: float, offset6: float, user: int, tool: int, *dyn_params: DynParam) -> Pose:
        """Run inverse kinematics from Cartesian pose to joint angles.

        Args:
            offset1: X position.
            offset2: Y position.
            offset3: Z position.
            offset4: RX rotation.
            offset5: RY rotation.
            offset6: RZ rotation.
            user: User coordinate index.
            tool: Tool coordinate index.
            *dyn_params: Optional solver parameters.

        Returns:
            Joint angles as ``(j1, j2, j3, j4, j5, j6)``.
        """
        return self.dashboard.inverse_solution(offset1, offset2, offset3, offset4, offset5, offset6, user, tool, *dyn_params)

    def lim_z(self, value: int) -> int:
        """Set maximum lifting height for door-type parameters.

        Args:
            value: Maximum lifting height.

        Returns:
            Command queue ID.
        """
        return self.dashboard.lim_z(value)

    def load_switch(self, offset1: int) -> int:
        """Switch load configuration.

        Args:
            offset1: Load profile index.

        Returns:
            Command queue ID.
        """
        return self.dashboard.load_switch(offset1)

    def modbus_close(self, offset1: int) -> int:
        """Close a Modbus connection.

        Returns:
            Command queue ID.
        """
        return self.dashboard.modbus_close(offset1)

    def modbus_create(self, ip: str, port: int, slave_id: int, is_rtu: int) -> int:
        """Create a Modbus connection.

        Args:
            ip: Modbus device IP address.
            port: Modbus device port.
            slave_id: Slave device identifier.
            is_rtu: Connection mode flag (0 for TCP, 1 for RTU).

        Returns:
            Created Modbus connection index.
        """
        return self.dashboard.modbus_create(ip, port, slave_id, is_rtu)

    def pause(self) -> int:
        """Pause queued motion execution.

        Returns:
            Command queue ID.
        """
        return self.dashboard.pause()

    def pause_script(self) -> int:
        """Pause the script.

        Returns:
            Command queue ID.
        """
        return self.dashboard.pause_script()

    def payload(self, weight: float, inertia: float) -> int:
        """Set robot load.

        Args:
            weight: Payload weight.
            inertia: Payload moment of inertia.

        Returns:
            Command queue ID.
        """
        return self.dashboard.payload(weight, inertia)

    def positive_solution(self, offset1: float, offset2: float, offset3: float, offset4: float, offset5: float, offset6: float, user: int, tool: int) -> Pose:
        """Run forward kinematics from joint angles to Cartesian pose.

        Args:
            offset1: Joint 1 angle.
            offset2: Joint 2 angle.
            offset3: Joint 3 angle.
            offset4: Joint 4 angle.
            offset5: Joint 5 angle.
            offset6: Joint 6 angle.
            user: User coordinate index.
            tool: Tool coordinate index.

        Returns:
            Cartesian pose as ``(x, y, z, rx, ry, rz)``.
        """
        return self.dashboard.positive_solution(offset1, offset2, offset3, offset4, offset5, offset6, user, tool)

    def power_on(self) -> int:
        """Power on the robot.

        Note: Takes ~10 s before the robot is enabled after power-on.

        Returns:
            Command queue ID.
        """
        return self.dashboard.power_on()

    def reset_robot(self) -> int:
        """Stop the robot.

        Returns:
            Command queue ID.
        """
        return self.dashboard.reset_robot()

    def resume(self) -> int:
        """Resume paused motion execution.

        Note: maps to the ``continue()`` protocol command; ``continue`` is a
        Python keyword so the method is named ``resume``.

        Returns:
            Command queue ID.
        """
        return self.dashboard.resume()

    def robot_mode(self) -> int:
        """View the robot status.

        Returns:
            Robot mode value as integer.
        """
        return self.dashboard.robot_mode()

    def run_script(self, project_name: str) -> int:
        """Run a script file.

        Args:
            project_name: Script file name.

        Returns:
            Command queue ID.
        """
        return self.dashboard.run_script(project_name)

    def set_arm_orientation(self, r: int, d: int, n: int, cfg: int) -> int:
        """Set the hand command.

        Args:
            r: Forward/backward selector (1 for forward, -1 for backward).
            d: Elbow orientation (1 for up, -1 for down).
            n: Wrist flip selector (1 for no flip, -1 for flip).
            cfg: Sixth-axis angle configuration identifier.

        Returns:
            Command queue ID.
        """
        return self.dashboard.set_arm_orientation(r, d, n, cfg)

    def set_coils(self, offset1: int, offset2: int, offset3: int, offset4: int) -> int:
        """Write coil values.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Coil count.
            offset4: Packed coil value.

        Returns:
            Command queue ID.
        """
        return self.dashboard.set_coils(offset1, offset2, offset3, offset4)

    def set_collide_drag(self, offset1: int) -> int:
        """Configure collision drag mode.

        Args:
            offset1: Drag mode flag.

        Returns:
            Command queue ID.
        """
        return self.dashboard.set_collide_drag(offset1)

    def set_collision_level(self, offset1: int) -> int:
        """Set collision detection level.

        Args:
            offset1: Collision level value.

        Returns:
            Command queue ID.
        """
        return self.dashboard.set_collision_level(offset1)

    def set_hold_regs(self, id: int, addr: int, count: int, table: str, type_: str | None = None) -> int:
        """Write hold register.

        Args:
            id: Secondary device number (0-4, where 0 is controller slave).
            addr: Starting hold-register address (3095-4095).
            count: Number of items to write (1-16).
            table: Register data payload string.
            type_: Optional data type, such as ``"U16"``, ``"U32"``,
                ``"F32"``, or ``"F64"``.

        Returns:
            Command queue ID.
        """
        return self.dashboard.set_hold_regs(id, addr, count, table, type_)

    def set_obstacle_avoid(self, offset1: int) -> int:
        """Configure obstacle avoidance feature.

        Returns:
            Command queue ID.
        """
        return self.dashboard.set_obstacle_avoid(offset1)

    def set_payload(self, offset1: float, *dyn_params: DynParam) -> int:
        """Set payload parameters.

        Args:
            offset1: Base payload value.
            *dyn_params: Additional payload arguments.

        Returns:
            Command queue ID.
        """
        return self.dashboard.set_payload(offset1, *dyn_params)

    def set_safe_skin(self, offset1: int) -> int:
        """Configure safe-skin feature.

        Returns:
            Command queue ID.
        """
        return self.dashboard.set_safe_skin(offset1)

    def set_terminal_485(self, offset1: int, offset2: int, offset3: str, offset4: int) -> int:
        """Set terminal RS-485 parameters.

        Args:
            offset1: Baud rate.
            offset2: Data bits.
            offset3: Parity setting.
            offset4: Stop bits.

        Returns:
            Command queue ID.
        """
        return self.dashboard.set_terminal_485(offset1, offset2, offset3, offset4)

    def set_terminal_keys(self, offset1: int) -> int:
        """Configure terminal key behavior.

        Args:
            offset1: Key mode value.

        Returns:
            Command queue ID.
        """
        return self.dashboard.set_terminal_keys(offset1)

    def set_tool(self, index: int) -> int:
        """Select the calibrated tool coordinate system.

        Args:
            index: Calibrated tool coordinate index.

        Returns:
            Command queue ID.
        """
        return self.dashboard.set_tool(index)

    def set_user(self, index: int) -> int:
        """Select the calibrated user coordinate system.

        Args:
            index: Calibrated user coordinate index.

        Returns:
            Command queue ID.
        """
        return self.dashboard.set_user(index)

    def speed_factor(self, speed: int) -> int:
        """Set global speed factor.

        Args:
            speed: Rate value in range 1-100.

        Returns:
            Command queue ID.

        Example:
            >>> dashboard.speed_factor(40)
        """
        return self.dashboard.speed_factor(speed)

    def speed_j(self, speed: int) -> int:
        """Set joint speed ratio (MovJ / MovJIO / MovJR / JointMovJ).

        Args:
            speed: Joint speed ratio (1-100).

        Returns:
            Command queue ID.
        """
        return self.dashboard.speed_j(speed)

    def speed_l(self, speed: int) -> int:
        """Set Cartesian speed ratio (MovL / MovLIO / MovLR / Jump / Arc / Circle).

        Args:
            speed: Cartesian speed ratio (1-100).

        Returns:
            Command queue ID.
        """
        return self.dashboard.speed_l(speed)

    def start_drag(self) -> int:
        """Enable drag mode.

        Returns:
            Command queue ID.
        """
        return self.dashboard.start_drag()

    def stop_drag(self) -> int:
        """Disable drag mode.

        Returns:
            Command queue ID.
        """
        return self.dashboard.stop_drag()

    def stop_script(self) -> int:
        """Stop scripts.

        Returns:
            Command queue ID.
        """
        return self.dashboard.stop_script()

    def tcp_speed(self, offset1: int) -> int:
        """Set TCP speed.

        Args:
            offset1: TCP speed value.

        Returns:
            Command queue ID.
        """
        return self.dashboard.tcp_speed(offset1)

    def tcp_speed_end(self) -> int:
        """End TCP speed mode.

        Returns:
            Command queue ID.
        """
        return self.dashboard.tcp_speed_end()

    def tool_di(self, offset1: int) -> int:
        """Read a terminal digital input port.

        Args:
            offset1: Terminal digital input index.

        Returns:
            Digital input state (0 or 1).
        """
        return self.dashboard.tool_di(offset1)

    def tool_do(self, index: int, status: int) -> int:
        """Set terminal signal output (queued).

        Args:
            index: Terminal output index (1-2).
            status: Output state (0 for low, 1 for high).

        Returns:
            Command queue ID.
        """
        return self.dashboard.tool_do(index, status)

    def tool_do_execute(self, index: int, status: int) -> int:
        """Set terminal signal output (immediate).

        Args:
            index: Terminal output index (1-2).
            status: Output state (0 for low, 1 for high).

        Returns:
            Command queue ID.
        """
        return self.dashboard.tool_do_execute(index, status)

    def vel_j(self, speed: int) -> int:
        """Alias for :meth:`speed_j` (V4-style name)."""
        return self.dashboard.vel_j(speed)

    def vel_l(self, speed: int) -> int:
        """Alias for :meth:`speed_l` (V4-style name)."""
        return self.dashboard.vel_l(speed)

    def wait(self, t: float) -> int:
        """Wait for specified time (queued command).

        Args:
            t: Wait duration in milliseconds.

        Returns:
            Command queue ID.
        """
        return self.dashboard.wait(t)

    # -- move -------------------------------------------------------------
    def arc(self, x1: float, y1: float, z1: float, a1: float, b1: float, c1: float, x2: float, y2: float, z2: float, a2: float, b2: float, c2: float, *dyn_params: DynParam) -> int:
        """Circular motion through an intermediate point.

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
            Command queue ID.
        """
        return self.move.arc(x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, *dyn_params)

    def circle3(self, x1: float, y1: float, z1: float, a1: float, b1: float, c1: float, x2: float, y2: float, z2: float, a2: float, b2: float, c2: float, count: int, *dyn_params: DynParam) -> int:
        """Full-circle motion command.

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
            count: Number of full rotations.
            *dyn_params: Optional motion parameters.

        Returns:
            Command queue ID.
        """
        return self.move.circle3(x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, count, *dyn_params)

    def joint_mov_j(self, j1: float, j2: float, j3: float, j4: float, j5: float, j6: float, *dyn_params: DynParam) -> int:
        """Joint motion interface (joint target).

        Args:
            j1: Target joint 1 angle.
            j2: Target joint 2 angle.
            j3: Target joint 3 angle.
            j4: Target joint 4 angle.
            j5: Target joint 5 angle.
            j6: Target joint 6 angle.
            *dyn_params: Optional motion parameters.

        Returns:
            Command queue ID.
        """
        return self.move.joint_mov_j(j1, j2, j3, j4, j5, j6, *dyn_params)

    def jump(self) -> None:
        """Placeholder for Jump command.

        This method is intentionally not implemented in the current version.
        """
        self.move.jump()

    def mov_j(self, x: float, y: float, z: float, rx: float, ry: float, rz: float, *dyn_params: DynParam) -> int:
        """Joint motion interface (point-to-point motion mode).

        Args:
            x: Target X coordinate.
            y: Target Y coordinate.
            z: Target Z coordinate.
            rx: Target RX rotation.
            ry: Target RY rotation.
            rz: Target RZ rotation.
            *dyn_params: Optional motion parameters.

        Returns:
            Command queue ID.

        Example:
            >>> move.mov_j(200, 0, 200, 0, 0, 0)
            >>> move.mov_j(220, 20, 180, 0, 0, 0, "SpeedJ=40", "AccJ=40")
        """
        return self.move.mov_j(x, y, z, rx, ry, rz, *dyn_params)

    def mov_j_io(self, x: float, y: float, z: float, a: float, b: float, c: float, *dyn_params: DynParam) -> int:
        """Point-to-point motion with parallel digital output control.

        Args:
            x: Target X coordinate.
            y: Target Y coordinate.
            z: Target Z coordinate.
            a: Target A rotation.
            b: Target B rotation.
            c: Target C rotation.
            *dyn_params: Parallel I/O tuples ``(mode, distance, index, status)``.

        Returns:
            Command queue ID.
        """
        return self.move.mov_j_io(x, y, z, a, b, c, *dyn_params)

    def mov_l(self, x: float, y: float, z: float, rx: float, ry: float, rz: float, *dyn_params: DynParam) -> int:
        """Linear motion interface.

        Args:
            x: Target X coordinate.
            y: Target Y coordinate.
            z: Target Z coordinate.
            rx: Target RX rotation.
            ry: Target RY rotation.
            rz: Target RZ rotation.
            *dyn_params: Optional motion parameters.

        Returns:
            Command queue ID.

        Example:
            >>> move.mov_l(250, 0, 180, 0, 0, 0)
            >>> move.mov_l(250, 30, 180, 0, 0, 0, "SpeedL=30", "AccL=30")
        """
        return self.move.mov_l(x, y, z, rx, ry, rz, *dyn_params)

    def mov_l_io(self, x: float, y: float, z: float, a: float, b: float, c: float, *dyn_params: DynParam) -> int:
        """Linear motion with parallel digital output control.

        Args:
            x: Target X coordinate.
            y: Target Y coordinate.
            z: Target Z coordinate.
            a: Target A rotation.
            b: Target B rotation.
            c: Target C rotation.
            *dyn_params: Parallel I/O tuples ``(mode, distance, index, status)``.

        Returns:
            Command queue ID.
        """
        return self.move.mov_l_io(x, y, z, a, b, c, *dyn_params)

    def move_jog(self, axis_id: str, *dyn_params: DynParam) -> int:
        """Jog motion along a single axis.

        Args:
            axis_id: Axis command such as ``"J1+"`` or ``"X-"``.
            *dyn_params: Optional jog parameters ``(coord_type, user, tool)``.

        Returns:
            Command queue ID.

        Example:
            >>> move.move_jog("J1+")
            >>> move.move_jog("")
        """
        return self.move.move_jog(axis_id, *dyn_params)

    def rel_joint_mov_j(self, offset1: float, offset2: float, offset3: float, offset4: float, offset5: float, offset6: float, *dyn_params: DynParam) -> int:
        """Relative motion along each joint axis (joint motion mode).

        Args:
            offset1: Joint 1 offset.
            offset2: Joint 2 offset.
            offset3: Joint 3 offset.
            offset4: Joint 4 offset.
            offset5: Joint 5 offset.
            offset6: Joint 6 offset.
            *dyn_params: Optional tuples such as ``(speed_j, acc_j)``.

        Returns:
            Command queue ID.
        """
        return self.move.rel_joint_mov_j(offset1, offset2, offset3, offset4, offset5, offset6, *dyn_params)

    def rel_mov_j(self, offset1: float, offset2: float, offset3: float, offset4: float, offset5: float, offset6: float, *dyn_params: DynParam) -> int:
        """Relative joint offset motion (point-to-point mode).

        Args:
            offset1: Joint 1 offset.
            offset2: Joint 2 offset.
            offset3: Joint 3 offset.
            offset4: Joint 4 offset.
            offset5: Joint 5 offset.
            offset6: Joint 6 offset.
            *dyn_params: Optional motion parameters.

        Returns:
            Command queue ID.
        """
        return self.move.rel_mov_j(offset1, offset2, offset3, offset4, offset5, offset6, *dyn_params)

    def rel_mov_j_tool(self, offset_x: float, offset_y: float, offset_z: float, offset_rx: float, offset_ry: float, offset_rz: float, tool: int, *dyn_params: ToolDynParam) -> int:
        """Relative joint motion along the tool coordinate system.

        Args:
            offset_x: X offset in tool frame.
            offset_y: Y offset in tool frame.
            offset_z: Z offset in tool frame.
            offset_rx: RX offset in tool frame.
            offset_ry: RY offset in tool frame.
            offset_rz: RZ offset in tool frame.
            tool: Tool coordinate index.
            *dyn_params: Optional tuples ``(speed_j, acc_j, user)``.

        Returns:
            Command queue ID.
        """
        return self.move.rel_mov_j_tool(offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, tool, *dyn_params)

    def rel_mov_j_user(self, offset_x: float, offset_y: float, offset_z: float, offset_rx: float, offset_ry: float, offset_rz: float, user: int, *dyn_params: DynParam) -> int:
        """Relative joint motion along the user coordinate system.

        Args:
            offset_x: X offset in user frame.
            offset_y: Y offset in user frame.
            offset_z: Z offset in user frame.
            offset_rx: RX offset in user frame.
            offset_ry: RY offset in user frame.
            offset_rz: RZ offset in user frame.
            user: User coordinate index.
            *dyn_params: Optional tuples ``(speed_j, acc_j, tool)``.

        Returns:
            Command queue ID.
        """
        return self.move.rel_mov_j_user(offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, user, *dyn_params)

    def rel_mov_l(self, offset_x: float, offset_y: float, offset_z: float, *dyn_params: DynParam) -> int:
        """Relative Cartesian offset motion (linear mode).

        Args:
            offset_x: X-axis offset.
            offset_y: Y-axis offset.
            offset_z: Z-axis offset.
            *dyn_params: Optional motion parameters.

        Returns:
            Command queue ID.
        """
        return self.move.rel_mov_l(offset_x, offset_y, offset_z, *dyn_params)

    def rel_mov_l_tool(self, offset_x: float, offset_y: float, offset_z: float, offset_rx: float, offset_ry: float, offset_rz: float, tool: int, *dyn_params: ToolDynParam) -> int:
        """Relative linear motion along the tool coordinate system.

        Args:
            offset_x: X offset in tool frame.
            offset_y: Y offset in tool frame.
            offset_z: Z offset in tool frame.
            offset_rx: RX offset in tool frame.
            offset_ry: RY offset in tool frame.
            offset_rz: RZ offset in tool frame.
            tool: Tool coordinate index.
            *dyn_params: Optional tuples ``(speed_l, acc_l, user)``.

        Returns:
            Command queue ID.
        """
        return self.move.rel_mov_l_tool(offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, tool, *dyn_params)

    def rel_mov_l_user(self, offset_x: float, offset_y: float, offset_z: float, offset_rx: float, offset_ry: float, offset_rz: float, user: int, *dyn_params: DynParam) -> int:
        """Relative linear motion along the user coordinate system.

        Args:
            offset_x: X offset in user frame.
            offset_y: Y offset in user frame.
            offset_z: Z offset in user frame.
            offset_rx: RX offset in user frame.
            offset_ry: RY offset in user frame.
            offset_rz: RZ offset in user frame.
            user: User coordinate index.
            *dyn_params: Optional tuples ``(speed_l, acc_l, tool)``.

        Returns:
            Command queue ID.
        """
        return self.move.rel_mov_l_user(offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, user, *dyn_params)

    def servo_j(self, j1: float, j2: float, j3: float, j4: float, j5: float, j6: float, t: float = 0.1, lookahead_time: float = 50.0, gain: float = 500.0) -> int:
        """Dynamic following in joint space.

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
            Command queue ID.
        """
        return self.move.servo_j(j1, j2, j3, j4, j5, j6, t, lookahead_time, gain)

    def servo_js(self, j1: float, j2: float, j3: float, j4: float, j5: float, j6: float) -> int:
        """Dynamic following in joint space (simplified form).

        Args:
            j1: Target joint 1 angle.
            j2: Target joint 2 angle.
            j3: Target joint 3 angle.
            j4: Target joint 4 angle.
            j5: Target joint 5 angle.
            j6: Target joint 6 angle.

        Returns:
            Command queue ID.
        """
        return self.move.servo_js(j1, j2, j3, j4, j5, j6)

    def servo_p(self, x: float, y: float, z: float, a: float, b: float, c: float) -> int:
        """Dynamic following in Cartesian space.

        Args:
            x: Target X coordinate.
            y: Target Y coordinate.
            z: Target Z coordinate.
            a: Target A rotation.
            b: Target B rotation.
            c: Target C rotation.

        Returns:
            Command queue ID.
        """
        return self.move.servo_p(x, y, z, a, b, c)

    def start_fc_trace(self, trace_name: str) -> int:
        """Execute a trajectory file with force control (Cartesian points).

        Args:
            trace_name: Trajectory file name including suffix.

        Returns:
            Command queue ID.
        """
        return self.move.start_fc_trace(trace_name)

    def start_path(self, trace_name: str, const: int, cart: int) -> int:
        """Replay a trajectory file (joint points).

        Args:
            trace_name: Trajectory file name including suffix.
            const: Constant-speed mode flag.
            cart: Cartesian/joint path flag.

        Returns:
            Command queue ID.
        """
        return self.move.start_path(trace_name, const, cart)

    def start_trace(self, trace_name: str) -> int:
        """Execute a trajectory file (Cartesian points).

        Args:
            trace_name: Trajectory file name including suffix.

        Returns:
            Command queue ID.
        """
        return self.move.start_trace(trace_name)

    def sync(self) -> int:
        """Block until all queued commands have been executed.

        Returns:
            Command queue ID.

        Example:
            >>> move.mov_j(200, 0, 200, 0, 0, 0)
            >>> move.mov_l(220, 20, 180, 0, 0, 0)
            >>> move.sync()
        """
        return self.move.sync()

    # --- END AUTO-GENERATED ---

    def __repr__(self) -> str:
        return f"DobotRobot(ip={self.ip!r})"
