"""Dashboard API for Dobot robot configuration and control commands."""

from __future__ import annotations

from typing import Any

from dobot_api.base import DobotApi


class DobotApiDashboard(DobotApi):
    """Dashboard API for robot configuration and control.

    This class provides commands for enabling/disabling the robot, setting
    parameters, controlling I/O, and managing robot state. All commands
    are sent through port 29999.

    Example:
        dashboard = DobotApiDashboard("192.168.1.6", 29999)
        dashboard.EnableRobot()
        dashboard.SpeedFactor(50)

    """

    # ==================== Robot Control ====================

    def EnableRobot(
        self,
        load: float = 0.0,
        centerX: float = 0.0,
        centerY: float = 0.0,
        centerZ: float = 0.0,
    ) -> str:
        """Enable the robot.

        Args:
            load: Load weight in kg (default: 0.0)
            centerX: Load center X offset (default: 0.0)
            centerY: Load center Y offset (default: 0.0)
            centerZ: Load center Z offset (default: 0.0)

        Returns:
            Response string from robot

        """
        cmd = "EnableRobot("
        if load != 0:
            cmd += f"{load:f}"
            if centerX != 0 or centerY != 0 or centerZ != 0:
                cmd += f",{centerX:f},{centerY:f},{centerZ:f}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    def DisableRobot(self) -> str:
        """Disable the robot."""
        return self.sendRecvMsg("DisableRobot()")

    def ClearError(self) -> str:
        """Clear controller alarm information."""
        return self.sendRecvMsg("ClearError()")

    def ResetRobot(self) -> str:
        """Stop and reset the robot."""
        return self.sendRecvMsg("ResetRobot()")

    def PowerOn(self) -> str:
        """Power on the robot.

        Note: It takes about 10 seconds for the robot to be enabled after power on.
        """
        return self.sendRecvMsg("PowerOn()")

    def EmergencyStop(self) -> str:
        """Trigger emergency stop."""
        return self.sendRecvMsg("EmergencyStop()")

    # ==================== Speed & Acceleration ====================

    def SpeedFactor(self, speed: int) -> str:
        """Set the global speed ratio.

        Args:
            speed: Speed ratio (1-100)

        """
        return self.sendRecvMsg(f"SpeedFactor({speed:d})")

    def SpeedJ(self, speed: int) -> str:
        """Set joint speed ratio (for MovJ, MovJIO, MovJR, JointMovJ).

        Args:
            speed: Joint velocity ratio (1-100)

        """
        return self.sendRecvMsg(f"SpeedJ({speed:d})")

    def SpeedL(self, speed: int) -> str:
        """Set cartesian speed ratio (for MovL, MovLIO, MovLR, Jump, Arc, Circle).

        Args:
            speed: Cartesian velocity ratio (1-100)

        """
        return self.sendRecvMsg(f"SpeedL({speed:d})")

    def AccJ(self, speed: int) -> str:
        """Set joint acceleration ratio (for MovJ, MovJIO, MovJR, JointMovJ).

        Args:
            speed: Joint acceleration ratio (1-100)

        """
        return self.sendRecvMsg(f"AccJ({speed:d})")

    def AccL(self, speed: int) -> str:
        """Set cartesian acceleration ratio (for MovL, MovLIO, MovLR, Jump, Arc, Circle).

        Args:
            speed: Cartesian acceleration ratio (1-100)

        """
        return self.sendRecvMsg(f"AccL({speed:d})")

    def TCPSpeed(self, speed: int) -> str:
        """Set TCP speed."""
        return self.sendRecvMsg(f"TCPSpeed({speed:d})")

    def TCPSpeedEnd(self) -> str:
        """End TCP speed setting."""
        return self.sendRecvMsg("TCPSpeedEnd()")

    # ==================== Coordinate Systems ====================

    def User(self, index: int) -> str:
        """Select user coordinate system.

        Args:
            index: User coordinate system index

        """
        return self.sendRecvMsg(f"User({index:d})")

    def Tool(self, index: int) -> str:
        """Select tool coordinate system.

        Args:
            index: Tool coordinate system index

        """
        return self.sendRecvMsg(f"Tool({index:d})")

    def SetArmOrientation(self, r: int, d: int = 0, n: int = 0, cfg: int = 0) -> str:
        """Set the arm orientation.

        Args:
            r: Arm direction, forward/backward (1: forward, -1: backward)
            d: Elbow direction (1: up elbow, -1: down elbow)
            n: Wrist flip (1: no flip, -1: flip)
            cfg: Sixth axis angle identification

        """
        if d == 0 and n == 0 and cfg == 0:
            return self.sendRecvMsg(f"SetArmOrientation({r:d})")
        return self.sendRecvMsg(f"SetArmOrientation({r:d},{d:d},{n:d},{cfg:d})")

    # ==================== Load & Payload ====================

    def PayLoad(self, weight: float, inertia: float) -> str:
        """Set robot load parameters.

        Args:
            weight: Load weight in kg
            inertia: Load moment of inertia

        """
        return self.sendRecvMsg(f"PayLoad({weight:f},{inertia:f})")

    def SetPayload(self, weight: float, *dynParams) -> str:
        """Set payload with optional parameters.

        Args:
            weight: Load weight in kg
            *dynParams: Additional parameters

        """
        cmd = f"SetPayload({weight:f}"
        for param in dynParams:
            cmd += f",{param}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    # ==================== Digital I/O ====================

    def DO(self, index: int, status: int) -> str:
        """Set digital output (queued).

        Args:
            index: Digital output index (1-24)
            status: Output state (0: low, 1: high)

        """
        return self.sendRecvMsg(f"DO({index:d},{status:d})")

    def DOExecute(self, index: int, status: int) -> str:
        """Set digital output (immediate).

        Args:
            index: Digital output index (1-24)
            status: Output state (0: low, 1: high)

        """
        return self.sendRecvMsg(f"DOExecute({index:d},{status:d})")

    def DI(self, index: int) -> str:
        """Read digital input.

        Args:
            index: Digital input index

        """
        return self.sendRecvMsg(f"DI({index:d})")

    def DOGroup(self, *dynParams) -> str:
        """Set multiple digital outputs."""
        cmd = "DOGroup("
        cmd += ",".join(str(p) for p in dynParams)
        cmd += ")"
        self.send_data(cmd)
        return self.wait_reply()

    # ==================== Tool I/O ====================

    def ToolDO(self, index: int, status: int) -> str:
        """Set terminal digital output (queued).

        Args:
            index: Terminal output index (1-2)
            status: Output state (0: low, 1: high)

        """
        return self.sendRecvMsg(f"ToolDO({index:d},{status:d})")

    def ToolDOExecute(self, index: int, status: int) -> str:
        """Set terminal digital output (immediate).

        Args:
            index: Terminal output index (1-2)
            status: Output state (0: low, 1: high)

        """
        return self.sendRecvMsg(f"ToolDOExecute({index:d},{status:d})")

    def ToolDI(self, index: int) -> str:
        """Read terminal digital input.

        Args:
            index: Terminal input index

        """
        return self.sendRecvMsg(f"DI({index:d})")

    # ==================== Analog I/O ====================

    def AO(self, index: int, val: float) -> str:
        """Set analog output (queued).

        Args:
            index: Analog output index (1-2)
            val: Voltage value (0-10V)

        """
        return self.sendRecvMsg(f"AO({index:d},{val:f})")

    def AOExecute(self, index: int, val: float) -> str:
        """Set analog output (immediate).

        Args:
            index: Analog output index (1-2)
            val: Voltage value (0-10V)

        """
        return self.sendRecvMsg(f"AOExecute({index:d},{val:f})")

    # ==================== Motion Parameters ====================

    def Arch(self, index: int) -> str:
        """Set Jump gate parameter index.

        Args:
            index: Parameter index (0-9)

        """
        return self.sendRecvMsg(f"Arch({index:d})")

    def CP(self, ratio: int) -> str:
        """Set smooth transition ratio.

        Args:
            ratio: Smooth transition ratio (1-100)

        """
        return self.sendRecvMsg(f"CP({ratio:d})")

    def LimZ(self, value: int) -> str:
        """Set maximum lifting height for door-type parameters.

        Args:
            value: Maximum lifting height

        """
        return self.sendRecvMsg(f"LimZ({value:d})")

    # ==================== Robot State ====================

    def RobotMode(self) -> str:
        """Get current robot mode/status."""
        return self.sendRecvMsg("RobotMode()")

    def GetErrorID(self) -> str:
        """Get robot error codes."""
        return self.sendRecvMsg("GetErrorID()")

    def GetAngle(self) -> str:
        """Get current joint angles."""
        return self.sendRecvMsg("GetAngle()")

    def GetPose(self) -> str:
        """Get current TCP pose."""
        return self.sendRecvMsg("GetPose()")

    def GetSixForceData(self) -> str:
        """Get six-axis force sensor data."""
        return self.sendRecvMsg("GetSixForceData()")

    # ==================== Kinematics ====================

    def PositiveSolution(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        user: int,
        tool: int,
    ) -> str:
        """Compute forward kinematics.

        Args:
            j1-j6: Joint angles
            user: User coordinate system index
            tool: Tool coordinate system index

        """
        return self.sendRecvMsg(
            f"PositiveSolution({j1:f},{j2:f},{j3:f},{j4:f},{j5:f},{j6:f},{user:d},{tool:d})"
        )

    def InverseSolution(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
        user: int,
        tool: int,
        *dynParams,
    ) -> str:
        """Compute inverse kinematics.

        Args:
            x, y, z: Cartesian position
            rx, ry, rz: Orientation
            user: User coordinate system index
            tool: Tool coordinate system index
            *dynParams: Additional parameters

        """
        cmd = f"InverseSolution({x:f},{y:f},{z:f},{rx:f},{ry:f},{rz:f},{user:d},{tool:d}"
        for param in dynParams:
            cmd += repr(param)
        cmd += ")"
        return self.sendRecvMsg(cmd)

    # ==================== Modbus ====================

    def ModbusCreate(self, ip: str, port: int, slave_id: int, isRTU: int) -> str:
        """Create Modbus connection.

        Args:
            ip: Modbus device IP
            port: Modbus port
            slave_id: Slave ID
            isRTU: RTU mode (0: TCP, 1: RTU)

        """
        return self.sendRecvMsg(f"ModbusCreate({ip},{port:d},{slave_id:d},{isRTU:d})")

    def ModbusClose(self, index: int) -> str:
        """Close Modbus connection.

        Args:
            index: Modbus connection index

        """
        return self.sendRecvMsg(f"ModbusClose({index:d})")

    def GetHoldRegs(self, id: int, addr: int, count: int, type: str = "U16") -> str:
        """Read holding registers.

        Args:
            id: Secondary device number (0-4, 0 for internal slave)
            addr: Starting register address (3095-4095)
            count: Number of registers to read (1-16)
            type: Data type ("U16", "U32", "F32", "F64")

        """
        return self.sendRecvMsg(f"GetHoldRegs({id:d},{addr:d},{count:d},{type})")

    def SetHoldRegs(
        self,
        id: int,
        addr: int,
        count: int,
        table: str,
        type: str | None = None,
    ) -> str:
        """Write holding registers.

        Args:
            id: Secondary device number (0-4)
            addr: Starting register address (3095-4095)
            count: Number of registers to write (1-16)
            table: Data to write
            type: Data type (optional)

        """
        if type is not None:
            return self.sendRecvMsg(f"SetHoldRegs({id:d},{addr:d},{count:d},{table},{type})")
        return self.sendRecvMsg(f"SetHoldRegs({id:d},{addr:d},{count:d},{table})")

    def GetInBits(self, id: int, addr: int, count: int) -> str:
        """Read input bits."""
        return self.sendRecvMsg(f"GetInBits({id:d},{addr:d},{count:d})")

    def GetInRegs(self, id: int, addr: int, count: int, *dynParams) -> str:
        """Read input registers."""
        cmd = f"GetInRegs({id:d},{addr:d},{count:d}"
        for param in dynParams:
            cmd += param[0]
        cmd += ")"
        return self.sendRecvMsg(cmd)

    def GetCoils(self, id: int, addr: int, count: int) -> str:
        """Read coils."""
        return self.sendRecvMsg(f"GetCoils({id:d},{addr:d},{count:d})")

    def SetCoils(self, id: int, addr: int, count: int, data: Any) -> str:
        """Write coils."""
        return self.sendRecvMsg(f"SetCoils({id:d},{addr:d},{count:d},{repr(data)})")

    # ==================== Scripts ====================

    def RunScript(self, project_name: str) -> str:
        """Run a script file.

        Args:
            project_name: Script file name

        """
        return self.sendRecvMsg(f"RunScript({project_name})")

    def StopScript(self) -> str:
        """Stop running script."""
        return self.sendRecvMsg("StopScript()")

    def PauseScript(self) -> str:
        """Pause running script."""
        return self.sendRecvMsg("PauseScript()")

    def ContinueScript(self) -> str:
        """Continue paused script."""
        return self.sendRecvMsg("ContinueScript()")

    # ==================== Drag Mode ====================

    def StartDrag(self) -> str:
        """Enable drag/teach mode."""
        return self.sendRecvMsg("StartDrag()")

    def StopDrag(self) -> str:
        """Disable drag/teach mode."""
        return self.sendRecvMsg("StopDrag()")

    def SetCollideDrag(self, status: int) -> str:
        """Set collision drag mode.

        Args:
            status: Enable/disable (0/1)

        """
        return self.sendRecvMsg(f"SetCollideDrag({status:d})")

    # ==================== Safety ====================

    def SetCollisionLevel(self, level: int) -> str:
        """Set collision detection level.

        Args:
            level: Collision detection level

        """
        return self.sendRecvMsg(f"SetCollisionLevel({level:d})")

    def SetSafeSkin(self, status: int) -> str:
        """Enable/disable safe skin.

        Args:
            status: Enable/disable (0/1)

        """
        return self.sendRecvMsg(f"SetSafeSkin({status:d})")

    def SetObstacleAvoid(self, status: int) -> str:
        """Enable/disable obstacle avoidance.

        Args:
            status: Enable/disable (0/1)

        """
        return self.sendRecvMsg(f"SetObstacleAvoid({status:d})")

    # ==================== Terminal & Brake ====================

    def SetTerminalKeys(self, status: int) -> str:
        """Set terminal keys status."""
        return self.sendRecvMsg(f"SetTerminalKeys({status:d})")

    def SetTerminal485(self, baud: int, data_bits: int, parity: str, stop_bits: int) -> str:
        """Configure terminal RS485.

        Args:
            baud: Baud rate
            data_bits: Data bits
            parity: Parity ("N", "E", "O")
            stop_bits: Stop bits

        """
        return self.sendRecvMsg(f"SetTerminal485({baud:d},{data_bits:d},{parity},{stop_bits:d})")

    def GetTerminal485(self) -> str:
        """Get terminal RS485 configuration."""
        return self.sendRecvMsg("GetTerminal485()")

    def BrakeControl(self, axis: int, status: int) -> str:
        """Control axis brake.

        Args:
            axis: Axis number
            status: Brake status (0/1)

        """
        return self.sendRecvMsg(f"BrakeControl({axis:d},{status:d})")

    def LoadSwitch(self, status: int) -> str:
        """Switch load mode.

        Args:
            status: Load switch status

        """
        return self.sendRecvMsg(f"LoadSwitch({status:d})")

    # ==================== Trajectory ====================

    def GetTraceStartPose(self, name: str) -> str:
        """Get trajectory start pose.

        Args:
            name: Trajectory file name

        """
        return self.sendRecvMsg(f"GetTraceStartPose({name})")

    def GetPathStartPose(self, name: str) -> str:
        """Get path start pose.

        Args:
            name: Path file name

        """
        return self.sendRecvMsg(f"GetPathStartPose({name})")

    def HandleTrajPoints(self, name: str) -> str:
        """Handle trajectory points.

        Args:
            name: Trajectory name

        """
        return self.sendRecvMsg(f"HandleTrajPoints({name})")

    # ==================== Flow Control ====================

    def wait(self, t: int) -> str:
        """Wait for specified time.

        Args:
            t: Wait time in ms

        """
        return self.sendRecvMsg(f"wait({t:d})")

    def pause(self) -> str:
        """Pause execution."""
        return self.sendRecvMsg("pause()")

    def Continue(self) -> str:
        """Continue execution."""
        return self.sendRecvMsg("continue()")
