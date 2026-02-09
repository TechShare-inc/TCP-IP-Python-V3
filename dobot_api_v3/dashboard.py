"""Dashboard/control commands for Dobot API."""

from __future__ import annotations

from .base import DobotApi


class DobotApiDashboard(DobotApi):
    """Dashboard class for robot control commands. Connects to dashboard port (29999)."""

    def _fmt(self, value):
        if isinstance(value, (list, tuple)):
            return "{" + ",".join(self._fmt(item) for item in value) + "}"
        if isinstance(value, float):
            return "{:f}".format(value)
        if isinstance(value, int):
            return "{:d}".format(value)
        return str(value)

    def _build_cmd(self, name, *args, **kwargs):
        parts = [self._fmt(item) for item in args]
        parts.extend(f"{k}={self._fmt(v)}" for k, v in kwargs.items())
        return f"{name}(" + ",".join(parts) + ")"

    # V4-style method aliases for consistent naming.
    def VelJ(self, speed):
        return self.SpeedJ(speed)

    def VelL(self, speed):
        return self.SpeedL(speed)

    def Pause(self):
        return self.pause()

    def Stop(self):
        return self.ResetRobot()

    def EnableRobot(self, load=0.0, centerX=0.0, centerY=0.0, centerZ=0.0):
        string = "EnableRobot("
        if load != 0:
            string = string + "{:f}".format(load)
            if centerX != 0 or centerY != 0 or centerZ != 0:
                string = string + ",{:f},{:f},{:f}".format(centerX, centerY, centerZ)
        string = string + ")"
        return self.sendRecvMsg(string)

    def DisableRobot(self):
        """
        Disabled the robot
        """
        string = "DisableRobot()"
        return self.sendRecvMsg(string)

    def ClearError(self):
        """
        Clear controller alarm information
        """
        string = "ClearError()"
        return self.sendRecvMsg(string)

    def ResetRobot(self):
        """
        Robot stop
        """
        string = "ResetRobot()"
        return self.sendRecvMsg(string)

    def SpeedFactor(self, speed):
        """
        Setting the Global rate
        speed:Rate value(Value range:1~100)
        """
        string = "SpeedFactor({:d})".format(speed)
        return self.sendRecvMsg(string)

    def User(self, index):
        """
        Select the calibrated user coordinate system
        index : Calibrated index of user coordinates
        """
        string = "User({:d})".format(index)
        return self.sendRecvMsg(string)

    def Tool(self, index):
        """
        Select the calibrated tool coordinate system
        index : Calibrated index of tool coordinates
        """
        string = "Tool({:d})".format(index)
        return self.sendRecvMsg(string)

    def RobotMode(self):
        """
        View the robot status
        """
        string = "RobotMode()"
        return self.sendRecvMsg(string)

    def PayLoad(self, weight, inertia):
        """
        Setting robot load
        weight : The load weight
        inertia: The load moment of inertia
        """
        string = "PayLoad({:f},{:f})".format(weight, inertia)
        return self.sendRecvMsg(string)

    def DO(self, index, status):
        """
        Set digital signal output (Queue instruction)
        index : Digital output index (Value range:1~24)
        status : Status of digital signal output port(0:Low level,1:High level
        """
        string = "DO({:d},{:d})".format(index, status)
        return self.sendRecvMsg(string)

    def DOExecute(self, index, status):
        """
        Set digital signal output (Instructions immediately)
        index : Digital output index (Value range:1~24)
        status : Status of digital signal output port(0:Low level,1:High level)
        """
        string = "DOExecute({:d},{:d})".format(index, status)
        return self.sendRecvMsg(string)

    def ToolDO(self, index, status):
        """
        Set terminal signal output (Queue instruction)
        index : Terminal output index (Value range:1~2)
        status : Status of digital signal output port(0:Low level,1:High level)
        """
        string = "ToolDO({:d},{:d})".format(index, status)
        return self.sendRecvMsg(string)

    def ToolDOExecute(self, index, status):
        """
        Set terminal signal output (Instructions immediately)
        index : Terminal output index (Value range:1~2)
        status : Status of digital signal output port(0:Low level,1:High level)
        """
        string = "ToolDOExecute({:d},{:d})".format(index, status)
        return self.sendRecvMsg(string)

    def AO(self, index, val):
        """
        Set analog signal output (Queue instruction)
        index : Analog output index (Value range:1~2)
        val : Voltage value (0~10)
        """
        string = "AO({:d},{:f})".format(index, val)
        return self.sendRecvMsg(string)

    def AOExecute(self, index, val):
        """
        Set analog signal output (Instructions immediately)
        index : Analog output index (Value range:1~2)
        val : Voltage value (0~10)
        """
        string = "AOExecute({:d},{:f})".format(index, val)
        return self.sendRecvMsg(string)

    def AccJ(self, speed):
        """
        Set joint acceleration ratio (Only for MovJ, MovJIO, MovJR, JointMovJ commands)
        speed : Joint acceleration ratio (Value range:1~100)
        """
        string = "AccJ({:d})".format(speed)
        return self.sendRecvMsg(string)

    def AccL(self, speed):
        """
        Set the coordinate system acceleration ratio (Only for MovL, MovLIO, MovLR, Jump, Arc, Circle commands)
        speed : Cartesian acceleration ratio (Value range:1~100)
        """
        string = "AccL({:d})".format(speed)
        return self.sendRecvMsg(string)

    def SpeedJ(self, speed):
        """
        Set joint speed ratio (Only for MovJ, MovJIO, MovJR, JointMovJ commands)
        speed : Joint velocity ratio (Value range:1~100)
        """
        string = "SpeedJ({:d})".format(speed)
        return self.sendRecvMsg(string)

    def SpeedL(self, speed):
        """
        Set the cartesian acceleration ratio (Only for MovL, MovLIO, MovLR, Jump, Arc, Circle commands)
        speed : Cartesian acceleration ratio (Value range:1~100)
        """
        string = "SpeedL({:d})".format(speed)
        return self.sendRecvMsg(string)

    def Arch(self, index):
        """
        Set the Jump gate parameter index (This index contains: start point lift height, maximum lift height, end point drop height)
        index : Parameter index (Value range:0~9)
        """
        string = "Arch({:d})".format(index)
        return self.sendRecvMsg(string)

    def CP(self, ratio):
        """
        Set smooth transition ratio
        ratio : Smooth transition ratio (Value range:1~100)
        """
        string = "CP({:d})".format(ratio)
        return self.sendRecvMsg(string)

    def LimZ(self, value):
        """
        Set the maximum lifting height of door type parameters
        value : Maximum lifting height (Highly restricted:Do not exceed the limit position of the z-axis of the manipulator)
        """
        string = "LimZ({:d})".format(value)
        return self.sendRecvMsg(string)

    def SetArmOrientation(self, r, d, n, cfg):
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
        return self.sendRecvMsg(string)

    def PowerOn(self):
        """
        Powering on the robot
        Note: It takes about 10 seconds for the robot to be enabled after it is powered on.
        """
        string = "PowerOn()"
        return self.sendRecvMsg(string)

    def RunScript(self, project_name):
        """
        Run the script file
        project_name :Script file name
        """
        string = "RunScript({:s})".format(project_name)
        return self.sendRecvMsg(string)

    def StopScript(self):
        """
        Stop scripts
        """
        string = "StopScript()"
        return self.sendRecvMsg(string)

    def PauseScript(self):
        """
        Pause the script
        """
        string = "PauseScript()"
        return self.sendRecvMsg(string)

    def ContinueScript(self):
        """
        Continue running the script
        """
        string = "ContinueScript()"
        return self.sendRecvMsg(string)

    def GetHoldRegs(self, id, addr, count, type):
        """
        Read hold register
        id :Secondary device NUMBER (A maximum of five devices can be supported. The value ranges from 0 to 4
            Set to 0 when accessing the internal slave of the controller)
        addr :Hold the starting address of the register (Value range:3095~4095)
        count :Reads the specified number of types of data (Value range:1~16)
        type :The data type
            If null, the 16-bit unsigned integer (2 bytes, occupying 1 register) is read by default
            "U16" : reads 16-bit unsigned integers (2 bytes, occupying 1 register)
            "U32" : reads 32-bit unsigned integers (4 bytes, occupying 2 registers)
            "F32" : reads 32-bit single-precision floating-point number (4 bytes, occupying 2 registers)
            "F64" : reads 64-bit double precision floating point number (8 bytes, occupying 4 registers)
        """
        string = "GetHoldRegs({:d},{:d},{:d},{:s})".format(id, addr, count, type)
        return self.sendRecvMsg(string)

    def SetHoldRegs(self, id, addr, count, table, type=None):
        """
        Write hold register
        id :Secondary device NUMBER (A maximum of five devices can be supported. The value ranges from 0 to 4
            Set to 0 when accessing the internal slave of the controller)
        addr :Hold the starting address of the register (Value range:3095~4095)
        count :Writes the specified number of types of data (Value range:1~16)
        type :The data type
            If null, the 16-bit unsigned integer (2 bytes, occupying 1 register) is read by default
            "U16" : reads 16-bit unsigned integers (2 bytes, occupying 1 register)
            "U32" : reads 32-bit unsigned integers (4 bytes, occupying 2 registers)
            "F32" : reads 32-bit single-precision floating-point number (4 bytes, occupying 2 registers)
            "F64" : reads 64-bit double precision floating point number (8 bytes, occupying 4 registers)
        """
        if type is not None:
            string = "SetHoldRegs({:d},{:d},{:d},{:s},{:s})".format(
                id, addr, count, table, type
            )
        else:
            string = "SetHoldRegs({:d},{:d},{:d},{:s})".format(id, addr, count, table)
        return self.sendRecvMsg(string)

    def GetErrorID(self):
        """
        Get robot error code
        """
        string = "GetErrorID()"
        return self.sendRecvMsg(string)

    def SetPayload(self, offset1, *dynParams):
        string = "SetPayload({:f}".format(offset1)
        for params in dynParams:
            string = string + str(params) + ","
        string = string + ")"
        return self.sendRecvMsg(string)

    def PositiveSolution(
        self, offset1, offset2, offset3, offset4, offset5, offset6, user, tool
    ):
        string = (
            "PositiveSolution({:f},{:f},{:f},{:f},{:f},{:f},{:d},{:d}".format(
                offset1, offset2, offset3, offset4, offset5, offset6, user, tool
            )
            + ")"
        )
        return self.sendRecvMsg(string)

    def InverseSolution(
        self,
        offset1,
        offset2,
        offset3,
        offset4,
        offset5,
        offset6,
        user,
        tool,
        *dynParams,
    ):
        string = "InverseSolution({:f},{:f},{:f},{:f},{:f},{:f},{:d},{:d}".format(
            offset1, offset2, offset3, offset4, offset5, offset6, user, tool
        )
        for params in dynParams:
            print(type(params), params)
            string = string + repr(params)
        string = string + ")"
        return self.sendRecvMsg(string)

    def SetCollisionLevel(self, offset1):
        string = "SetCollisionLevel({:d}".format(offset1) + ")"
        return self.sendRecvMsg(string)

    def GetAngle(self):
        string = "GetAngle()"
        return self.sendRecvMsg(string)

    def GetPose(self):
        string = "GetPose()"
        return self.sendRecvMsg(string)

    def EmergencyStop(self):
        string = "EmergencyStop()"
        return self.sendRecvMsg(string)

    def ModbusCreate(self, ip, port, slave_id, isRTU):
        string = (
            "ModbusCreate({:s},{:d},{:d},{:d}".format(ip, port, slave_id, isRTU) + ")"
        )
        return self.sendRecvMsg(string)

    def ModbusClose(self, offset1):
        string = "ModbusClose({:d}".format(offset1) + ")"
        return self.sendRecvMsg(string)

    def SetSafeSkin(self, offset1):
        string = "SetSafeSkin({:d}".format(offset1) + ")"
        return self.sendRecvMsg(string)

    def SetObstacleAvoid(self, offset1):
        string = "SetObstacleAvoid({:d}".format(offset1) + ")"
        return self.sendRecvMsg(string)

    def GetTraceStartPose(self, offset1):
        string = "GetTraceStartPose({:s}".format(offset1) + ")"
        return self.sendRecvMsg(string)

    def GetPathStartPose(self, offset1):
        string = "GetPathStartPose({:s}".format(offset1) + ")"
        return self.sendRecvMsg(string)

    def HandleTrajPoints(self, offset1):
        string = "HandleTrajPoints({:s}".format(offset1) + ")"
        return self.sendRecvMsg(string)

    def GetSixForceData(self):
        string = "GetSixForceData()"
        return self.sendRecvMsg(string)

    def SetCollideDrag(self, offset1):
        string = "SetCollideDrag({:d}".format(offset1) + ")"
        return self.sendRecvMsg(string)

    def SetTerminalKeys(self, offset1):
        string = "SetTerminalKeys({:d}".format(offset1) + ")"
        return self.sendRecvMsg(string)

    def SetTerminal485(self, offset1, offset2, offset3, offset4):
        string = (
            "SetTerminal485({:d},{:d},{:s},{:d}".format(
                offset1, offset2, offset3, offset4
            )
            + ")"
        )
        return self.sendRecvMsg(string)

    def GetTerminal485(self):
        string = "GetTerminal485()"
        return self.sendRecvMsg(string)

    def TCPSpeed(self, offset1):
        string = "TCPSpeed({:d}".format(offset1) + ")"
        return self.sendRecvMsg(string)

    def TCPSpeedEnd(self):
        string = "TCPSpeedEnd()"
        return self.sendRecvMsg(string)

    def GetInBits(self, offset1, offset2, offset3):
        string = "GetInBits({:d},{:d},{:d}".format(offset1, offset2, offset3) + ")"
        return self.sendRecvMsg(string)

    def GetInRegs(self, offset1, offset2, offset3, *dynParams):
        string = "GetInRegs({:d},{:d},{:d}".format(offset1, offset2, offset3)
        for params in dynParams:
            print(type(params), params)
            string = string + params[0]
        string = string + ")"
        return self.sendRecvMsg(string)

    def GetCoils(self, offset1, offset2, offset3):
        string = "GetCoils({:d},{:d},{:d}".format(offset1, offset2, offset3) + ")"
        return self.sendRecvMsg(string)

    def SetCoils(self, offset1, offset2, offset3, offset4):
        string = (
            "SetCoils({:d},{:d},{:d}".format(offset1, offset2, offset3)
            + ","
            + repr(offset4)
            + ")"
        )
        print(str(offset4))
        return self.sendRecvMsg(string)

    def DI(self, offset1):
        string = "DI({:d}".format(offset1) + ")"
        return self.sendRecvMsg(string)

    def ToolDI(self, offset1):
        string = "DI({:d}".format(offset1) + ")"
        return self.sendRecvMsg(string)

    def DOGroup(self, *dynParams):
        string = "DOGroup("
        for params in dynParams:
            string = string + str(params) + ","
        string = string + ")"
        print(string)
        return self.wait_reply()

    def BrakeControl(self, offset1, offset2):
        string = "BrakeControl({:d},{:d}".format(offset1, offset2) + ")"
        return self.sendRecvMsg(string)

    def StartDrag(self):
        string = "StartDrag()"
        return self.sendRecvMsg(string)

    def StopDrag(self):
        string = "StopDrag()"
        return self.sendRecvMsg(string)

    def LoadSwitch(self, offset1):
        string = "LoadSwitch({:d}".format(offset1) + ")"
        return self.sendRecvMsg(string)

    def wait(self, t):
        string = "wait({:d})".format(t)
        return self.sendRecvMsg(string)

    def pause(self):
        string = "pause()"
        return self.sendRecvMsg(string)

    def Continue(self):
        string = "continue()"
        return self.sendRecvMsg(string)

