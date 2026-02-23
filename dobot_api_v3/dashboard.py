"""Dashboard/control commands for Dobot API."""

from __future__ import annotations


from loguru import logger

from .base import DobotApi
from .utils import DynParam


class DobotApiDashboard(DobotApi):
    """Dashboard command client for Dobot control APIs.

    This class sends robot lifecycle, I/O, configuration, and status commands
    over the dashboard TCP port (usually ``29999``).
    """

    def _fmt(self, value: int | float | str | list | tuple) -> str:
        """Format one command argument into Dobot protocol text.

        Args:
            value: Scalar or collection argument value.

        Returns:
            Protocol-ready string representation.
        """
        if isinstance(value, (list, tuple)):
            return "{" + ",".join(self._fmt(item) for item in value) + "}"
        if isinstance(value, float):
            return "{:f}".format(value)
        if isinstance(value, int):
            return "{:d}".format(value)
        return str(value)

    def _build_cmd(
        self, name: str, *args: int | float | str, **kwargs: int | float | str
    ) -> str:
        """Build a Dobot protocol command string.

        Args:
            name: Protocol command name.
            *args: Positional command arguments.
            **kwargs: Keyword-style command arguments.

        Returns:
            Serialized command text.
        """
        parts = [self._fmt(item) for item in args]
        parts.extend(f"{k}={self._fmt(v)}" for k, v in kwargs.items())
        return f"{name}(" + ",".join(parts) + ")"

    # ------------------------------------------------------------------
    # Protocol command methods (snake_case — primary implementation).
    # ------------------------------------------------------------------

    def enable_robot(
        self,
        load: float = 0.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
    ) -> str:
        """Enable the robot with optional payload parameters.

        Args:
            load: Payload weight.
            center_x: Payload center offset on X axis.
            center_y: Payload center offset on Y axis.
            center_z: Payload center offset on Z axis.

        Returns:
            Robot response string.

        Example:
            >>> dashboard.enable_robot()
            >>> dashboard.enable_robot(load=0.5, center_x=0.0, center_y=0.0, center_z=0.05)
        """
        string = "EnableRobot("
        if load != 0:
            string = string + "{:f}".format(load)
            if center_x != 0 or center_y != 0 or center_z != 0:
                string = string + ",{:f},{:f},{:f}".format(center_x, center_y, center_z)
        string = string + ")"
        return self.send_recv_msg(string)

    def disable_robot(self) -> str:
        """Disable the robot."""
        return self.send_recv_msg("DisableRobot()")

    def clear_error(self) -> str:
        """Clear controller alarm information.

        Returns:
            Robot response string.

        Example:
            >>> dashboard.clear_error()
        """
        return self.send_recv_msg("ClearError()")

    def reset_robot(self) -> str:
        """Stop the robot."""
        return self.send_recv_msg("ResetRobot()")

    def speed_factor(self, speed: int) -> str:
        """Set global speed factor.

        Args:
            speed: Rate value in range 1-100.

        Returns:
            Robot response string.

        Example:
            >>> dashboard.speed_factor(40)
        """
        return self.send_recv_msg("SpeedFactor({:d})".format(speed))

    def set_user(self, index: int) -> str:
        """Select the calibrated user coordinate system.

        Args:
            index: Calibrated user coordinate index.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("User({:d})".format(index))

    def set_tool(self, index: int) -> str:
        """Select the calibrated tool coordinate system.

        Args:
            index: Calibrated tool coordinate index.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("Tool({:d})".format(index))

    def robot_mode(self) -> str:
        """View the robot status."""
        return self.send_recv_msg("RobotMode()")

    def payload(self, weight: float, inertia: float) -> str:
        """Set robot load.

        Args:
            weight: Payload weight.
            inertia: Payload moment of inertia.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("PayLoad({:f},{:f})".format(weight, inertia))

    def do_output(self, index: int, status: int) -> str:
        """Set digital signal output (queued).

        Args:
            index: Digital output index (1-24).
            status: Output state (0 for low, 1 for high).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("DO({:d},{:d})".format(index, status))

    def do_execute(self, index: int, status: int) -> str:
        """Set digital signal output (immediate).

        Args:
            index: Digital output index (1-24).
            status: Output state (0 for low, 1 for high).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("DOExecute({:d},{:d})".format(index, status))

    def tool_do(self, index: int, status: int) -> str:
        """Set terminal signal output (queued).

        Args:
            index: Terminal output index (1-2).
            status: Output state (0 for low, 1 for high).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("ToolDO({:d},{:d})".format(index, status))

    def tool_do_execute(self, index: int, status: int) -> str:
        """Set terminal signal output (immediate).

        Args:
            index: Terminal output index (1-2).
            status: Output state (0 for low, 1 for high).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("ToolDOExecute({:d},{:d})".format(index, status))

    def ao(self, index: int, val: float) -> str:
        """Set analog signal output (queued).

        Args:
            index: Analog output index (1-2).
            val: Output voltage (0-10).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("AO({:d},{:f})".format(index, val))

    def ao_execute(self, index: int, val: float) -> str:
        """Set analog signal output (immediate).

        Args:
            index: Analog output index (1-2).
            val: Output voltage (0-10).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("AOExecute({:d},{:f})".format(index, val))

    def acc_j(self, speed: int) -> str:
        """Set joint acceleration ratio (MovJ / MovJIO / MovJR / JointMovJ).

        Args:
            speed: Joint acceleration ratio (1-100).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("AccJ({:d})".format(speed))

    def acc_l(self, speed: int) -> str:
        """Set Cartesian acceleration ratio (MovL / MovLIO / MovLR / Jump / Arc / Circle).

        Args:
            speed: Cartesian acceleration ratio (1-100).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("AccL({:d})".format(speed))

    def speed_j(self, speed: int) -> str:
        """Set joint speed ratio (MovJ / MovJIO / MovJR / JointMovJ).

        Args:
            speed: Joint speed ratio (1-100).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("SpeedJ({:d})".format(speed))

    def speed_l(self, speed: int) -> str:
        """Set Cartesian speed ratio (MovL / MovLIO / MovLR / Jump / Arc / Circle).

        Args:
            speed: Cartesian speed ratio (1-100).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("SpeedL({:d})".format(speed))

    def vel_j(self, speed: int) -> str:
        """Alias for :meth:`speed_j` (V4-style name)."""
        return self.speed_j(speed)

    def vel_l(self, speed: int) -> str:
        """Alias for :meth:`speed_l` (V4-style name)."""
        return self.speed_l(speed)

    def arch(self, index: int) -> str:
        """Set Jump gate parameter index (start lift height, max lift, end drop).

        Args:
            index: Jump parameter index (0-9).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("Arch({:d})".format(index))

    def cp(self, ratio: int) -> str:
        """Set smooth transition ratio.

        Args:
            ratio: Smooth transition ratio (1-100).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("CP({:d})".format(ratio))

    def lim_z(self, value: int) -> str:
        """Set maximum lifting height for door-type parameters.

        Args:
            value: Maximum lifting height.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("LimZ({:d})".format(value))

    def set_arm_orientation(self, r: int, d: int, n: int, cfg: int) -> str:
        """Set the hand command.

        Args:
            r: Forward/backward selector (1 for forward, -1 for backward).
            d: Elbow orientation (1 for up, -1 for down).
            n: Wrist flip selector (1 for no flip, -1 for flip).
            cfg: Sixth-axis angle configuration identifier.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg(
            "SetArmOrientation({:d},{:d},{:d},{:d})".format(r, d, n, cfg)
        )

    def power_on(self) -> str:
        """Power on the robot.

        Note: Takes ~10 s before the robot is enabled after power-on.
        """
        return self.send_recv_msg("PowerOn()")

    def run_script(self, project_name: str) -> str:
        """Run a script file.

        Args:
            project_name: Script file name.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("RunScript({:s})".format(project_name))

    def stop_script(self) -> str:
        """Stop scripts."""
        return self.send_recv_msg("StopScript()")

    def pause_script(self) -> str:
        """Pause the script."""
        return self.send_recv_msg("PauseScript()")

    def continue_script(self) -> str:
        """Continue running the script."""
        return self.send_recv_msg("ContinueScript()")

    def get_hold_regs(self, id: int, addr: int, count: int, type_: str) -> str:
        """Read hold register.

        Args:
            id: Secondary device number (0-4, where 0 is controller slave).
            addr: Starting hold-register address (3095-4095).
            count: Number of items to read (1-16).
            type_: Data type, such as ``"U16"``, ``"U32"``, ``"F32"``, or
                ``"F64"``.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg(
            "GetHoldRegs({:d},{:d},{:d},{:s})".format(id, addr, count, type_)
        )

    def set_hold_regs(
        self, id: int, addr: int, count: int, table: str, type_: str | None = None
    ) -> str:
        """Write hold register.

        Args:
            id: Secondary device number (0-4, where 0 is controller slave).
            addr: Starting hold-register address (3095-4095).
            count: Number of items to write (1-16).
            table: Register data payload string.
            type_: Optional data type, such as ``"U16"``, ``"U32"``,
                ``"F32"``, or ``"F64"``.

        Returns:
            Robot response string.
        """
        if type_ is not None:
            string = "SetHoldRegs({:d},{:d},{:d},{:s},{:s})".format(
                id, addr, count, table, type_
            )
        else:
            string = "SetHoldRegs({:d},{:d},{:d},{:s})".format(id, addr, count, table)
        return self.send_recv_msg(string)

    def get_error_id(self) -> str:
        """Get robot error code."""
        return self.send_recv_msg("GetErrorID()")

    def set_payload(self, offset1: float, *dyn_params: DynParam) -> str:
        """Set payload parameters.

        Args:
            offset1: Base payload value.
            *dyn_params: Additional payload arguments.

        Returns:
            Robot response string.
        """
        string = "SetPayload({:f}".format(offset1)
        for params in dyn_params:
            string = string + str(params) + ","
        string = string + ")"
        return self.send_recv_msg(string)

    def positive_solution(
        self,
        offset1: float,
        offset2: float,
        offset3: float,
        offset4: float,
        offset5: float,
        offset6: float,
        user: int,
        tool: int,
    ) -> str:
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
            Robot response string.
        """
        string = (
            "PositiveSolution({:f},{:f},{:f},{:f},{:f},{:f},{:d},{:d}".format(
                offset1, offset2, offset3, offset4, offset5, offset6, user, tool
            )
            + ")"
        )
        return self.send_recv_msg(string)

    def inverse_solution(
        self,
        offset1: float,
        offset2: float,
        offset3: float,
        offset4: float,
        offset5: float,
        offset6: float,
        user: int,
        tool: int,
        *dyn_params: DynParam,
    ) -> str:
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
            Robot response string.
        """
        string = "InverseSolution({:f},{:f},{:f},{:f},{:f},{:f},{:d},{:d}".format(
            offset1, offset2, offset3, offset4, offset5, offset6, user, tool
        )
        for params in dyn_params:
            logger.debug(f"InverseSolution params: type={type(params)}, value={params}")
            string = string + repr(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def set_collision_level(self, offset1: int) -> str:
        """Set collision detection level.

        Args:
            offset1: Collision level value.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("SetCollisionLevel({:d})".format(offset1))

    def get_angle(self) -> str:
        """Get current joint angles."""
        return self.send_recv_msg("GetAngle()")

    def get_pose(self) -> str:
        """Get current Cartesian pose."""
        return self.send_recv_msg("GetPose()")

    def emergency_stop(self) -> str:
        """Trigger emergency stop."""
        return self.send_recv_msg("EmergencyStop()")

    def modbus_create(self, ip: str, port: int, slave_id: int, is_rtu: int) -> str:
        """Create a Modbus connection.

        Args:
            ip: Modbus device IP address.
            port: Modbus device port.
            slave_id: Slave device identifier.
            is_rtu: Connection mode flag (0 for TCP, 1 for RTU).

        Returns:
            Robot response string.
        """
        return self.send_recv_msg(
            "ModbusCreate({:s},{:d},{:d},{:d})".format(ip, port, slave_id, is_rtu)
        )

    def modbus_close(self, offset1: int) -> str:
        """Close a Modbus connection."""
        return self.send_recv_msg("ModbusClose({:d})".format(offset1))

    def set_safe_skin(self, offset1: int) -> str:
        """Configure safe-skin feature."""
        return self.send_recv_msg("SetSafeSkin({:d})".format(offset1))

    def set_obstacle_avoid(self, offset1: int) -> str:
        """Configure obstacle avoidance feature."""
        return self.send_recv_msg("SetObstacleAvoid({:d})".format(offset1))

    def get_trace_start_pose(self, offset1: str) -> str:
        """Get starting pose of a Cartesian trajectory file.

        Args:
            offset1: Trajectory file name.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("GetTraceStartPose({:s})".format(offset1))

    def get_path_start_pose(self, offset1: str) -> str:
        """Get starting pose of a joint path file.

        Args:
            offset1: Path file name.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("GetPathStartPose({:s})".format(offset1))

    def handle_traj_points(self, offset1: str) -> str:
        """Process a trajectory points file.

        Args:
            offset1: Trajectory file name.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("HandleTrajPoints({:s})".format(offset1))

    def get_six_force_data(self) -> str:
        """Read six-axis force sensor data."""
        return self.send_recv_msg("GetSixForceData()")

    def set_collide_drag(self, offset1: int) -> str:
        """Configure collision drag mode.

        Args:
            offset1: Drag mode flag.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("SetCollideDrag({:d})".format(offset1))

    def set_terminal_keys(self, offset1: int) -> str:
        """Configure terminal key behavior.

        Args:
            offset1: Key mode value.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("SetTerminalKeys({:d})".format(offset1))

    def set_terminal_485(
        self, offset1: int, offset2: int, offset3: str, offset4: int
    ) -> str:
        """Set terminal RS-485 parameters.

        Args:
            offset1: Baud rate.
            offset2: Data bits.
            offset3: Parity setting.
            offset4: Stop bits.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg(
            "SetTerminal485({:d},{:d},{:s},{:d})".format(
                offset1, offset2, offset3, offset4
            )
        )

    def get_terminal_485(self) -> str:
        """Get terminal RS-485 configuration."""
        return self.send_recv_msg("GetTerminal485()")

    def tcp_speed(self, offset1: int) -> str:
        """Set TCP speed.

        Args:
            offset1: TCP speed value.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("TCPSpeed({:d})".format(offset1))

    def tcp_speed_end(self) -> str:
        """End TCP speed mode."""
        return self.send_recv_msg("TCPSpeedEnd()")

    def get_in_bits(self, offset1: int, offset2: int, offset3: int) -> str:
        """Read digital input bits.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Number of bits.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg(
            "GetInBits({:d},{:d},{:d})".format(offset1, offset2, offset3)
        )

    def get_in_regs(
        self, offset1: int, offset2: int, offset3: int, *dyn_params: DynParam
    ) -> str:
        """Read input registers.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Register count.
            *dyn_params: Optional data type and mode parameters.

        Returns:
            Robot response string.
        """
        string = "GetInRegs({:d},{:d},{:d}".format(offset1, offset2, offset3)
        for params in dyn_params:
            logger.debug(f"GetInRegs params: type={type(params)}, value={params}")
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def get_coils(self, offset1: int, offset2: int, offset3: int) -> str:
        """Read coil values.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Coil count.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg(
            "GetCoils({:d},{:d},{:d})".format(offset1, offset2, offset3)
        )

    def set_coils(self, offset1: int, offset2: int, offset3: int, offset4: int) -> str:
        """Write coil values.

        Args:
            offset1: Device identifier.
            offset2: Start address.
            offset3: Coil count.
            offset4: Packed coil value.

        Returns:
            Robot response string.
        """
        string = (
            "SetCoils({:d},{:d},{:d}".format(offset1, offset2, offset3)
            + ","
            + repr(offset4)
            + ")"
        )
        logger.debug(f"SetCoils offset4 value: {offset4}")
        return self.send_recv_msg(string)

    def di(self, offset1: int) -> str:
        """Read a digital input port.

        Args:
            offset1: Digital input index.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("DI({:d})".format(offset1))

    def tool_di(self, offset1: int) -> str:
        """Read a terminal digital input port.

        Args:
            offset1: Terminal digital input index.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("ToolDI({:d})".format(offset1))

    def do_group(self, *dyn_params: DynParam) -> str:
        """Set multiple digital outputs in one command.

        Args:
            *dyn_params: Repeating output pairs such as ``(index, status)``.

        Returns:
            Robot response string.
        """
        string = "DOGroup("
        for params in dyn_params:
            string = string + str(params) + ","
        string = string + ")"
        logger.debug(f"DOGroup command: {string}")
        return self.send_recv_msg(string)

    def brake_control(self, offset1: int, offset2: int) -> str:
        """Control joint brakes.

        Args:
            offset1: Joint index.
            offset2: Brake control value.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("BrakeControl({:d},{:d})".format(offset1, offset2))

    def start_drag(self) -> str:
        """Enable drag mode."""
        return self.send_recv_msg("StartDrag()")

    def stop_drag(self) -> str:
        """Disable drag mode."""
        return self.send_recv_msg("StopDrag()")

    def load_switch(self, offset1: int) -> str:
        """Switch load configuration.

        Args:
            offset1: Load profile index.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("LoadSwitch({:d})".format(offset1))

    def wait(self, t: float) -> str:
        """Wait for specified time (queued command).

        Args:
            t: Wait duration in milliseconds.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("wait({:d})".format(t))

    def pause(self) -> str:
        """Pause queued motion execution."""
        return self.send_recv_msg("pause()")

    def resume(self) -> str:
        """Resume paused motion execution.

        Note: maps to the ``continue()`` protocol command; ``continue`` is a
        Python keyword so the method is named ``resume``.
        """
        return self.send_recv_msg("continue()")

