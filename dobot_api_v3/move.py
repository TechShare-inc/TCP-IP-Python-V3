"""Movement commands for Dobot API (DobotApiMove class)."""

from __future__ import annotations

from loguru import logger

from .base import DobotApi
from .utils import DynParam, ToolDynParam


class DobotApiMove(DobotApi):
    """Movement class for robot motion commands. Connects to move port (30003)."""

    def MovJ(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
        *dynParams: DynParam,
    ) -> str:
        """
        Joint motion interface (point-to-point motion mode)
        x: A number in the Cartesian coordinate system x
        y: A number in the Cartesian coordinate system y
        z: A number in the Cartesian coordinate system z
        rx: Position of Rx axis in Cartesian coordinate system
        ry: Position of Ry axis in Cartesian coordinate system
        rz: Position of Rz axis in Cartesian coordinate system
        """
        string = "MovJ({:f},{:f},{:f},{:f},{:f},{:f}".format(x, y, z, rx, ry, rz)
        for params in dynParams:
            string = string + "," + str(params)
        string = string + ")"
        logger.debug(f"MovJ command: {string}")
        return self.send_recv_msg(string)

    def MovL(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
        *dynParams: DynParam,
    ) -> str:
        """
        Coordinate system motion interface (linear motion mode)
        x: A number in the Cartesian coordinate system x
        y: A number in the Cartesian coordinate system y
        z: A number in the Cartesian coordinate system z
        rx: Position of Rx axis in Cartesian coordinate system
        ry: Position of Ry axis in Cartesian coordinate system
        rz: Position of Rz axis in Cartesian coordinate system
        """
        string = "MovL({:f},{:f},{:f},{:f},{:f},{:f}".format(x, y, z, rx, ry, rz)
        for params in dynParams:
            string = string + "," + str(params)
        string = string + ")"
        logger.debug(f"MovL command: {string}")
        return self.send_recv_msg(string)

    def JointMovJ(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        *dynParams: DynParam,
    ) -> str:
        """
        Joint motion interface (linear motion mode)
        j1~j6:Point position values on each joint
        """
        string = "JointMovJ({:f},{:f},{:f},{:f},{:f},{:f}".format(
            j1, j2, j3, j4, j5, j6
        )
        for params in dynParams:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def Jump(self) -> None:
        logger.warning("TODO: Jump method not yet implemented.")

    def RelMovJ(
        self,
        offset1: float,
        offset2: float,
        offset3: float,
        offset4: float,
        offset5: float,
        offset6: float,
        *dynParams: DynParam,
    ) -> str:
        """
        Offset motion interface (point-to-point motion mode)
        j1~j6:Point position values on each joint
        """
        string = "RelMovJ({:f},{:f},{:f},{:f},{:f},{:f}".format(
            offset1, offset2, offset3, offset4, offset5, offset6
        )
        for params in dynParams:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def RelMovL(
        self, offsetX: float, offsetY: float, offsetZ: float, *dynParams: DynParam
    ) -> str:
        """
        Offset motion interface (point-to-point motion mode)
        x: Offset in the Cartesian coordinate system x
        y: offset in the Cartesian coordinate system y
        z: Offset in the Cartesian coordinate system Z
        """
        string = "RelMovL({:f},{:f},{:f}".format(offsetX, offsetY, offsetZ)
        for params in dynParams:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def MovLIO(
        self,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
        *dynParams: DynParam,
    ) -> str:
        """
        Set the digital output port state in parallel while moving in a straight line
        x: A number in the Cartesian coordinate system x
        y: A number in the Cartesian coordinate system y
        z: A number in the Cartesian coordinate system z
        a: A number in the Cartesian coordinate system a
        b: A number in the Cartesian coordinate system b
        c: a number in the Cartesian coordinate system c
        *dynParams :Parameter Settings（Mode、Distance、Index、Status）
                    Mode :Set Distance mode (0: Distance percentage; 1: distance from starting point or target point)
                    Distance :Runs the specified distance（If Mode is 0, the value ranges from 0 to 100；When Mode is 1, if the value is positive,
                             it indicates the distance from the starting point. If the value of Distance is negative, it represents the Distance from the target point）
                    Index :Digital output index （Value range:1~24）
                    Status :Digital output state（Value range:0/1）
        """
        # example: MovLIO(0,50,0,0,0,0,(0,50,1,0),(1,1,2,1))
        string = "MovLIO({:f},{:f},{:f},{:f},{:f},{:f}".format(x, y, z, a, b, c)
        for params in dynParams:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def MovJIO(
        self,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
        *dynParams: DynParam,
    ) -> str:
        """
        Set the digital output port state in parallel during point-to-point motion
        x: A number in the Cartesian coordinate system x
        y: A number in the Cartesian coordinate system y
        z: A number in the Cartesian coordinate system z
        a: A number in the Cartesian coordinate system a
        b: A number in the Cartesian coordinate system b
        c: a number in the Cartesian coordinate system c
        *dynParams :Parameter Settings（Mode、Distance、Index、Status）
                    Mode :Set Distance mode (0: Distance percentage; 1: distance from starting point or target point)
                    Distance :Runs the specified distance（If Mode is 0, the value ranges from 0 to 100；When Mode is 1, if the value is positive,
                             it indicates the distance from the starting point. If the value of Distance is negative, it represents the Distance from the target point）
                    Index :Digital output index （Value range:1~24）
                    Status :Digital output state（Value range:0/1）
        """
        # example: MovJIO(0,50,0,0,0,0,(0,50,1,0),(1,1,2,1))
        string = "MovJIO({:f},{:f},{:f},{:f},{:f},{:f}".format(x, y, z, a, b, c)
        logger.debug(f"MovJIO command: {string}")
        for params in dynParams:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def Arc(
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
        *dynParams: DynParam,
    ) -> str:
        """
        Circular motion instruction
        x1, y1, z1, a1, b1, c1 :Is the point value of intermediate point coordinates
        x2, y2, z2, a2, b2, c2 :Is the value of the end point coordinates
        Note: This instruction should be used together with other movement instructions
        """
        string = (
            "Arc({:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f}".format(
                x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2
            )
        )
        for params in dynParams:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def Circle3(
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
        count: int,
        *dynParams: DynParam,
    ) -> str:
        """
        Full circle motion command
        count:Run laps
        x1, y1, z1, r1 :Is the point value of intermediate point coordinates
        x2, y2, z2, r2 :Is the value of the end point coordinates
        Note: This instruction should be used together with other movement instructions
        """
        string = "Circle3({:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:d}".format(
            x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, count
        )
        for params in dynParams:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def ServoJ(
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
        """
        Dynamic follow command based on joint space
        j1~j6:Point position values on each joint

        可选参数:t、lookahead_time、gain
        t float 该点位的运行时间,默认0.1,单位:s  取值范围:[0.02,3600.0]
        lookahead_time   float 作用类似于PID的D项,默认50,标量,无单位 取值范围:[20.0,100.0]
        gain float   目标位置的比例放大器,作用类似于PID的P项,  默认500,标量,无单位   取值范围:[200.0,1000.0]
        """
        string = "ServoJ({:f},{:f},{:f},{:f},{:f},{:f},t={:f},lookahead_time={:f},gain={:f})".format(
            j1, j2, j3, j4, j5, j6, t, lookahead_time, gain
        )
        return self.send_recv_msg(string)

    def ServoJS(
        self, j1: float, j2: float, j3: float, j4: float, j5: float, j6: float
    ) -> str:
        """
        功能:基于关节空间的动态跟随运动。
        格式:ServoJS(J1,J2,J3,J4,J5,J6)
        """
        string = "ServoJS({:f},{:f},{:f},{:f},{:f},{:f})".format(j1, j2, j3, j4, j5, j6)
        return self.send_recv_msg(string)

    def ServoP(self, x: float, y: float, z: float, a: float, b: float, c: float) -> str:
        """
        Dynamic following command based on Cartesian space
        x, y, z, a, b, c :Cartesian coordinate point value
        """
        string = "ServoP({:f},{:f},{:f},{:f},{:f},{:f})".format(x, y, z, a, b, c)
        return self.send_recv_msg(string)

    def MoveJog(self, axis_id: str, *dynParams: DynParam) -> str:
        """
        Joint motion
        axis_id: Joint motion axis, optional string value:
            J1+ J2+ J3+ J4+ J5+ J6+
            J1- J2- J3- J4- J5- J6-
            X+ Y+ Z+ Rx+ Ry+ Rz+
            X- Y- Z- Rx- Ry- Rz-
        *dynParams: Parameter Settings（coord_type, user_index, tool_index）
                    coord_type: 1: User coordinate 2: tool coordinate (default value is 1)
                    user_index: user index is 0 ~ 9 (default value is 0)
                    tool_index: tool index is 0 ~ 9 (default value is 0)
        """
        string = "MoveJog({:s}".format(axis_id)
        for params in dynParams:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def StartTrace(self, trace_name: str) -> str:
        """
        Trajectory fitting (track file Cartesian points)
        trace_name: track file name (including suffix)
        (The track path is stored in /dobot/userdata/project/process/trajectory/)

        It needs to be used together with `GetTraceStartPose(recv_string.json)` interface
        """
        string = f"StartTrace({trace_name})"
        return self.send_recv_msg(string)

    def StartPath(self, trace_name: str, const: int, cart: int) -> str:
        """
        Track reproduction. (track file joint points)
        trace_name: track file name (including suffix)
        (The track path is stored in /dobot/userdata/project/process/trajectory/)
        const: When const = 1, it repeats at a constant speed, and the pause and dead zone in the track will be removed;
               When const = 0, reproduce according to the original speed;
        cart: When cart = 1, reproduce according to Cartesian path;
              When cart = 0, reproduce according to the joint path;

        It needs to be used together with `GetTraceStartPose(recv_string.json)` interface
        """
        string = f"StartPath({trace_name}, {const}, {cart})"
        return self.send_recv_msg(string)

    def StartFCTrace(self, trace_name: str) -> str:
        """
        Trajectory fitting with force control. (track file Cartesian points)
        trace_name: track file name (including suffix)
        (The track path is stored in /dobot/userdata/project/process/trajectory/)

        It needs to be used together with `GetTraceStartPose(recv_string.json)` interface
        """
        string = f"StartFCTrace({trace_name})"
        return self.send_recv_msg(string)

    def Sync(self) -> str:
        """
        The blocking program executes the queue instruction and returns after all the queue instructions are executed
        """
        string = "Sync()"
        return self.send_recv_msg(string)

    def RelMovJTool(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        tool: int,
        *dynParams: ToolDynParam,
    ) -> str:
        """
        The relative motion command is carried out along the tool coordinate system, and the end motion mode is joint motion
        offset_x: X-axis direction offset
        offset_y: Y-axis direction offset
        offset_z: Z-axis direction offset
        offset_rx: Rx axis position
        offset_ry: Ry axis position
        offset_rz: Rz axis position
        tool: Select the calibrated tool coordinate system, value range: 0 ~ 9
        *dynParams: parameter Settings（speed_j, acc_j, user）
                    speed_j: Set joint speed scale, value range: 1 ~ 100
                    acc_j: Set acceleration scale value, value range: 1 ~ 100
                    user: Set user coordinate system index
        """
        string = "RelMovJTool({:f},{:f},{:f},{:f},{:f},{:f}, {:d}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, tool
        )
        for params in dynParams:
            logger.debug(f"RelMovJTool params: type={type(params)}, value={params}")
            string = string + ", SpeedJ={:d}, AccJ={:d}, User={:d}".format(
                params[0], params[1], params[2]
            )
        string = string + ")"
        return self.send_recv_msg(string)

    def RelMovLTool(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        tool: int,
        *dynParams: ToolDynParam,
    ) -> str:
        """
        Carry out relative motion command along the tool coordinate system, and the end motion mode is linear motion
        offset_x: X-axis direction offset
        offset_y: Y-axis direction offset
        offset_z: Z-axis direction offset
        offset_rx: Rx axis position
        offset_ry: Ry axis position
        offset_rz: Rz axis position
        tool: Select the calibrated tool coordinate system, value range: 0 ~ 9
        *dynParams: parameter Settings（speed_l, acc_l, user）
                    speed_l: Set Cartesian speed scale, value range: 1 ~ 100
                    acc_l: Set acceleration scale value, value range: 1 ~ 100
                    user: Set user coordinate system index
        """
        string = "RelMovLTool({:f},{:f},{:f},{:f},{:f},{:f}, {:d}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, tool
        )
        for params in dynParams:
            logger.debug(f"RelMovLTool params: type={type(params)}, value={params}")
            string = string + ", SpeedJ={:d}, AccJ={:d}, User={:d}".format(
                params[0], params[1], params[2]
            )
        string = string + ")"
        return self.send_recv_msg(string)

    def RelMovJUser(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        user: int,
        *dynParams: DynParam,
    ) -> str:
        """
        The relative motion command is carried out along the user coordinate system, and the end motion mode is joint motion
        offset_x: X-axis direction offset
        offset_y: Y-axis direction offset
        offset_z: Z-axis direction offset
        offset_rx: Rx axis position
        offset_ry: Ry axis position
        offset_rz: Rz axis position

        user: Select the calibrated user coordinate system, value range: 0 ~ 9
        *dynParams: parameter Settings（speed_j, acc_j, tool）
                    speed_j: Set joint speed scale, value range: 1 ~ 100
                    acc_j: Set acceleration scale value, value range: 1 ~ 100
                    tool: Set tool coordinate system index
        """
        string = "RelMovJUser({:f},{:f},{:f},{:f},{:f},{:f}, {:d}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, user
        )
        for params in dynParams:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def RelMovLUser(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        user: int,
        *dynParams: DynParam,
    ) -> str:
        """
        The relative motion command is carried out along the user coordinate system, and the end motion mode is linear motion
        offset_x: X-axis direction offset
        offset_y: Y-axis direction offset
        offset_z: Z-axis direction offset
        offset_rx: Rx axis position
        offset_ry: Ry axis position
        offset_rz: Rz axis position
        user: Select the calibrated user coordinate system, value range: 0 ~ 9
        *dynParams: parameter Settings（speed_l, acc_l, tool）
                    speed_l: Set Cartesian speed scale, value range: 1 ~ 100
                    acc_l: Set acceleration scale value, value range: 1 ~ 100
                    tool: Set tool coordinate system index
        """
        string = "RelMovLUser({:f},{:f},{:f},{:f},{:f},{:f}, {:d}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, user
        )
        for params in dynParams:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def RelJointMovJ(
        self,
        offset1: float,
        offset2: float,
        offset3: float,
        offset4: float,
        offset5: float,
        offset6: float,
        *dynParams: DynParam,
    ) -> str:
        """
        The relative motion command is carried out along the joint coordinate system of each axis, and the end motion mode is joint motion
        Offset motion interface (point-to-point motion mode)
        j1~j6:Point position values on each joint
        *dynParams: parameter Settings（speed_j, acc_j, user）
                    speed_j: Set Cartesian speed scale, value range: 1 ~ 100
                    acc_j: Set acceleration scale value, value range: 1 ~ 100
        """
        string = "RelJointMovJ({:f},{:f},{:f},{:f},{:f},{:f}".format(
            offset1, offset2, offset3, offset4, offset5, offset6
        )
        for params in dynParams:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)
