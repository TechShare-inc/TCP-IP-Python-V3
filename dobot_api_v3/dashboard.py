"""Dashboard/control commands for Dobot API."""

from __future__ import annotations

from loguru import logger

from .base import DobotApi
from .utils import DynParam


class DobotApiDashboard(DobotApi):
    """Dashboard class for robot control commands. Connects to dashboard port (29999)."""

    def _fmt(self, value: int | float | str | list | tuple) -> str:
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
        parts = [self._fmt(item) for item in args]
        parts.extend(f"{k}={self._fmt(v)}" for k, v in kwargs.items())
        return f"{name}(" + ",".join(parts) + ")"

    # V4-style method aliases for consistent naming.
    def VelJ(self, speed: int) -> str:
        return self.SpeedJ(speed)

    def VelL(self, speed: int) -> str:
        return self.SpeedL(speed)

    def Pause(self) -> str:
        return self.pause()

    def Stop(self) -> str:
        return self.ResetRobot()

    def EnableRobot(
        self,
        load: float = 0.0,
        centerX: float = 0.0,
        centerY: float = 0.0,
        centerZ: float = 0.0,
    ) -> str:
        string = "EnableRobot("
        if load != 0:
            string = string + "{:f}".format(load)
            if centerX != 0 or centerY != 0 or centerZ != 0:
                string = string + ",{:f},{:f},{:f}".format(centerX, centerY, centerZ)
        string = string + ")"
        return self.send_recv_msg(string)

    def DisableRobot(self) -> str:
        """
        Disabled the robot
        """
        string = "DisableRobot()"
        return self.send_recv_msg(string)

    def ClearError(self) -> str:
        """
        Clear controller alarm information
        """
        string = "ClearError()"
        return self.send_recv_msg(string)

    def ResetRobot(self) -> str:
        """
        Robot stop
        """
        string = "ResetRobot()"
        return self.send_recv_msg(string)

    def SpeedFactor(self, speed: int) -> str:
        """
        Setting the Global rate
        speed:Rate value(Value range:1~100)
        """
        string = "SpeedFactor({:d})".format(speed)
        return self.send_recv_msg(string)

    def User(self, index: int) -> str:
        """
        Select the calibrated user coordinate system
        index : Calibrated index of user coordinates
        """
        string = "User({:d})".format(index)
        return self.send_recv_msg(string)

    def Tool(self, index: int) -> str:
        """
        Select the calibrated tool coordinate system
        index : Calibrated index of tool coordinates
        """
        string = "Tool({:d})".format(index)
        return self.send_recv_msg(string)

    def RobotMode(self) -> str:
        """
        View the robot status
        """
        string = "RobotMode()"
        return self.send_recv_msg(string)

    def PayLoad(self, weight: float, inertia: float) -> str:
        """
        Setting robot load
        weight : The load weight
        inertia: The load moment of inertia
        """
        string = "PayLoad({:f},{:f})".format(weight, inertia)
        return self.send_recv_msg(string)

    def DO(self, index: int, status: int) -> str:
        """
        Set digital signal output (Queue instruction)
        index : Digital output index (Value range:1~24)
        status : Status of digital signal output port(0:Low level,1:High level
        """
        string = "DO({:d},{:d})".format(index, status)
        return self.send_recv_msg(string)

    def DOExecute(self, index: int, status: int) -> str:
        """
        Set digital signal output (Instructions immediately)
        index : Digital output index (Value range:1~24)
        status : Status of digital signal output port(0:Low level,1:High level)
        """
        string = "DOExecute({:d},{:d})".format(index, status)
        return self.send_recv_msg(string)

    def ToolDO(self, index: int, status: int) -> str:
        """
        Set terminal signal output (Queue instruction)
        index : Terminal output index (Value range:1~2)
        status : Status of digital signal output port(0:Low level,1:High level)
        """
        string = "ToolDO({:d},{:d})".format(index, status)
        return self.send_recv_msg(string)

    def ToolDOExecute(self, index: int, status: int) -> str:
        """
        Set terminal signal output (Instructions immediately)
        index : Terminal output index (Value range:1~2)
        status : Status of digital signal output port(0:Low level,1:High level)
        """
        string = "ToolDOExecute({:d},{:d})".format(index, status)
        return self.send_recv_msg(string)

    def AO(self, index: int, val: float) -> str:
        """
        Set analog signal output (Queue instruction)
        index : Analog output index (Value range:1~2)
        val : Voltage value (0~10)
        """
        string = "AO({:d},{:f})".format(index, val)
        return self.send_recv_msg(string)

    def AOExecute(self, index: int, val: float) -> str:
        """
        Set analog signal output (Instructions immediately)
        index : Analog output index (Value range:1~2)
        val : Voltage value (0~10)
        """
        string = "AOExecute({:d},{:f})".format(index, val)
        return self.send_recv_msg(string)

    def AccJ(self, speed: int) -> str:
        """
        Set joint acceleration ratio (Only for MovJ, MovJIO, MovJR, JointMovJ commands)
        speed : Joint acceleration ratio (Value range:1~100)
        """
        string = "AccJ({:d})".format(speed)
        return self.send_recv_msg(string)

    def AccL(self, speed: int) -> str:
        """
        Set the coordinate system acceleration ratio (Only for MovL, MovLIO, MovLR, Jump, Arc, Circle commands)
        speed : Cartesian acceleration ratio (Value range:1~100)
        """
        string = "AccL({:d})".format(speed)
        return self.send_recv_msg(string)

    def SpeedJ(self, speed: int) -> str:
        """
        Set joint speed ratio (Only for MovJ, MovJIO, MovJR, JointMovJ commands)
        speed : Joint velocity ratio (Value range:1~100)
        """
        string = "SpeedJ({:d})".format(speed)
        return self.send_recv_msg(string)

    def SpeedL(self, speed: int) -> str:
        """
        Set the cartesian acceleration ratio (Only for MovL, MovLIO, MovLR, Jump, Arc, Circle commands)
        speed : Cartesian acceleration ratio (Value range:1~100)
        """
        string = "SpeedL({:d})".format(speed)
        return self.send_recv_msg(string)

    def Arch(self, index: int) -> str:
        """
        Set the Jump gate parameter index (This index contains: start point lift height, maximum lift height, end point drop height)
        index : Parameter index (Value range:0~9)
        """
        string = "Arch({:d})".format(index)
        return self.send_recv_msg(string)

    def CP(self, ratio: int) -> str:
        """
        Set smooth transition ratio
        ratio : Smooth transition ratio (Value range:1~100)
        """
        string = "CP({:d})".format(ratio)
        return self.send_recv_msg(string)

    def LimZ(self, value: int) -> str:
        """
        Set the maximum lifting height of door type parameters
        value : Maximum lifting height (Highly restricted:Do not exceed the limit position of the z-axis of the manipulator)
        """
        string = "LimZ({:d})".format(value)
        return self.send_recv_msg(string)

    def SetArmOrientation(self, r: int, d: int, n: int, cfg: int) -> str:
        """
        Set the hand command
        r : Mechanical arm direction, forward/backward (1:forward -1:backward)
        d : Mechanical arm direction, up elbow/down elbow (1:up elbow -1:down elbow)
        n : Whether the wrist of the mechanical arm is flipped (1:The wrist does not flip -1:The wrist flip)
        cfg :Sixth axis Angle identification
            (1, - 2... : Axis 6 Angle is [0,-90] is -1; [90, 180] - 2; And so on
            1, 2... : axis 6 Angle is [0,90] is 1; [90180] 2; And so on)
        """
        string = "SetArmOrientation({:d},{:d},{:d},{:d})".format(r, d, n, cfg)
        return self.send_recv_msg(string)

    def PowerOn(self) -> str:
        """
        Powering on the robot
        Note: It takes about 10 seconds for the robot to be enabled after it is powered on.
        """
        string = "PowerOn()"
        return self.send_recv_msg(string)

    def RunScript(self, project_name: str) -> str:
        """
        Run the script file
        project_name :Script file name
        """
        string = "RunScript({:s})".format(project_name)
        return self.send_recv_msg(string)

    def StopScript(self) -> str:
        """
        Stop scripts
        """
        string = "StopScript()"
        return self.send_recv_msg(string)

    def PauseScript(self) -> str:
        """
        Pause the script
        """
        string = "PauseScript()"
        return self.send_recv_msg(string)

    def ContinueScript(self) -> str:
        """
        Continue running the script
        """
        string = "ContinueScript()"
        return self.send_recv_msg(string)

    def GetHoldRegs(self, id: int, addr: int, count: int, type_: str) -> str:
        """
        Read hold register
        id :Secondary device NUMBER (A maximum of five devices can be supported. The value ranges from 0 to 4
            Set to 0 when accessing the internal slave of the controller)
        addr :Hold the starting address of the register (Value range:3095~4095)
        count :Reads the specified number of types of data (Value range:1~16)
        type_ :The data type
            If null, the 16-bit unsigned integer (2 bytes, occupying 1 register) is read by default
            "U16" : reads 16-bit unsigned integers (2 bytes, occupying 1 register)
            "U32" : reads 32-bit unsigned integers (4 bytes, occupying 2 registers)
            "F32" : reads 32-bit single-precision floating-point number (4 bytes, occupying 2 registers)
            "F64" : reads 64-bit double precision floating point number (8 bytes, occupying 4 registers)
        """
        string = "GetHoldRegs({:d},{:d},{:d},{:s})".format(id, addr, count, type_)
        return self.send_recv_msg(string)

    def SetHoldRegs(
        self, id: int, addr: int, count: int, table: str, type_: str | None = None
    ) -> str:
        """
        Write hold register
        id :Secondary device NUMBER (A maximum of five devices can be supported. The value ranges from 0 to 4
            Set to 0 when accessing the internal slave of the controller)
        addr :Hold the starting address of the register (Value range:3095~4095)
        count :Writes the specified number of types of data (Value range:1~16)
        type_ :The data type
            If null, the 16-bit unsigned integer (2 bytes, occupying 1 register) is read by default
            "U16" : reads 16-bit unsigned integers (2 bytes, occupying 1 register)
            "U32" : reads 32-bit unsigned integers (4 bytes, occupying 2 registers)
            "F32" : reads 32-bit single-precision floating-point number (4 bytes, occupying 2 registers)
            "F64" : reads 64-bit double precision floating point number (8 bytes, occupying 4 registers)
        """
        if type_ is not None:
            string = "SetHoldRegs({:d},{:d},{:d},{:s},{:s})".format(
                id, addr, count, table, type_
            )
        else:
            string = "SetHoldRegs({:d},{:d},{:d},{:s})".format(id, addr, count, table)
        return self.send_recv_msg(string)

    def GetErrorID(self) -> str:
        """
        Get robot error code
        """
        string = "GetErrorID()"
        return self.send_recv_msg(string)

    def SetPayload(self, offset1: float, *dynParams: DynParam) -> str:
        string = "SetPayload({:f}".format(offset1)
        for params in dynParams:
            string = string + str(params) + ","
        string = string + ")"
        return self.send_recv_msg(string)

    def PositiveSolution(
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
        string = (
            "PositiveSolution({:f},{:f},{:f},{:f},{:f},{:f},{:d},{:d}".format(
                offset1, offset2, offset3, offset4, offset5, offset6, user, tool
            )
            + ")"
        )
        return self.send_recv_msg(string)

    def InverseSolution(
        self,
        offset1: float,
        offset2: float,
        offset3: float,
        offset4: float,
        offset5: float,
        offset6: float,
        user: int,
        tool: int,
        *dynParams: DynParam,
    ) -> str:
        string = "InverseSolution({:f},{:f},{:f},{:f},{:f},{:f},{:d},{:d}".format(
            offset1, offset2, offset3, offset4, offset5, offset6, user, tool
        )
        for params in dynParams:
            logger.debug(f"InverseSolution params: type={type(params)}, value={params}")
            string = string + repr(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def SetCollisionLevel(self, offset1: int) -> str:
        string = "SetCollisionLevel({:d}".format(offset1) + ")"
        return self.send_recv_msg(string)

    def GetAngle(self) -> str:
        string = "GetAngle()"
        return self.send_recv_msg(string)

    def GetPose(self) -> str:
        string = "GetPose()"
        return self.send_recv_msg(string)

    def EmergencyStop(self) -> str:
        string = "EmergencyStop()"
        return self.send_recv_msg(string)

    def ModbusCreate(self, ip: str, port: int, slave_id: int, isRTU: int) -> str:
        string = (
            "ModbusCreate({:s},{:d},{:d},{:d}".format(ip, port, slave_id, isRTU) + ")"
        )
        return self.send_recv_msg(string)

    def ModbusClose(self, offset1: int) -> str:
        string = "ModbusClose({:d}".format(offset1) + ")"
        return self.send_recv_msg(string)

    def SetSafeSkin(self, offset1: int) -> str:
        string = "SetSafeSkin({:d}".format(offset1) + ")"
        return self.send_recv_msg(string)

    def SetObstacleAvoid(self, offset1: int) -> str:
        string = "SetObstacleAvoid({:d}".format(offset1) + ")"
        return self.send_recv_msg(string)

    def GetTraceStartPose(self, offset1: str) -> str:
        string = "GetTraceStartPose({:s}".format(offset1) + ")"
        return self.send_recv_msg(string)

    def GetPathStartPose(self, offset1: str) -> str:
        string = "GetPathStartPose({:s}".format(offset1) + ")"
        return self.send_recv_msg(string)

    def HandleTrajPoints(self, offset1: str) -> str:
        string = "HandleTrajPoints({:s}".format(offset1) + ")"
        return self.send_recv_msg(string)

    def GetSixForceData(self) -> str:
        string = "GetSixForceData()"
        return self.send_recv_msg(string)

    def SetCollideDrag(self, offset1: int) -> str:
        string = "SetCollideDrag({:d}".format(offset1) + ")"
        return self.send_recv_msg(string)

    def SetTerminalKeys(self, offset1: int) -> str:
        string = "SetTerminalKeys({:d}".format(offset1) + ")"
        return self.send_recv_msg(string)

    def SetTerminal485(
        self, offset1: int, offset2: int, offset3: str, offset4: int
    ) -> str:
        string = (
            "SetTerminal485({:d},{:d},{:s},{:d}".format(
                offset1, offset2, offset3, offset4
            )
            + ")"
        )
        return self.send_recv_msg(string)

    def GetTerminal485(self) -> str:
        string = "GetTerminal485()"
        return self.send_recv_msg(string)

    def TCPSpeed(self, offset1: int) -> str:
        string = "TCPSpeed({:d}".format(offset1) + ")"
        return self.send_recv_msg(string)

    def TCPSpeedEnd(self) -> str:
        string = "TCPSpeedEnd()"
        return self.send_recv_msg(string)

    def GetInBits(self, offset1: int, offset2: int, offset3: int) -> str:
        string = "GetInBits({:d},{:d},{:d}".format(offset1, offset2, offset3) + ")"
        return self.send_recv_msg(string)

    def GetInRegs(
        self, offset1: int, offset2: int, offset3: int, *dynParams: DynParam
    ) -> str:
        string = "GetInRegs({:d},{:d},{:d}".format(offset1, offset2, offset3)
        for params in dynParams:
            logger.debug(f"GetInRegs params: type={type(params)}, value={params}")
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def GetCoils(self, offset1: int, offset2: int, offset3: int) -> str:
        string = "GetCoils({:d},{:d},{:d}".format(offset1, offset2, offset3) + ")"
        return self.send_recv_msg(string)

    def SetCoils(self, offset1: int, offset2: int, offset3: int, offset4: int) -> str:
        string = (
            "SetCoils({:d},{:d},{:d}".format(offset1, offset2, offset3)
            + ","
            + repr(offset4)
            + ")"
        )
        logger.debug(f"SetCoils offset4 value: {offset4}")
        return self.send_recv_msg(string)

    def DI(self, offset1: int) -> str:
        string = "DI({:d}".format(offset1) + ")"
        return self.send_recv_msg(string)

    def ToolDI(self, offset1: int) -> str:
        string = "ToolDI({:d}".format(offset1) + ")"
        return self.send_recv_msg(string)

    def DOGroup(self, *dynParams: DynParam) -> str:
        string = "DOGroup("
        for params in dynParams:
            string = string + str(params) + ","
        string = string + ")"
        logger.debug(f"DOGroup command: {string}")
        return self.send_recv_msg(string)

    def BrakeControl(self, offset1: int, offset2: int) -> str:
        string = "BrakeControl({:d},{:d}".format(offset1, offset2) + ")"
        return self.send_recv_msg(string)

    def StartDrag(self) -> str:
        string = "StartDrag()"
        return self.send_recv_msg(string)

    def StopDrag(self) -> str:
        string = "StopDrag()"
        return self.send_recv_msg(string)

    def LoadSwitch(self, offset1: int) -> str:
        string = "LoadSwitch({:d}".format(offset1) + ")"
        return self.send_recv_msg(string)

    def wait(self, t: float) -> str:
        string = "wait({:d})".format(t)
        return self.send_recv_msg(string)

    def pause(self) -> str:
        string = "pause()"
        return self.send_recv_msg(string)

    def Continue(self) -> str:
        string = "continue()"
        return self.send_recv_msg(string)
