"""Movement commands for Dobot API (DobotApiMove class)."""

from __future__ import annotations

from .base import DobotApi


class DobotApiMove(DobotApi):
    """Movement class for robot motion commands. Connects to move port (30003)."""

    def MovJ(self, x, y, z, rx, ry, rz, *dynParams):
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
        print(string)
        return self.sendRecvMsg(string)

    def MovL(self, x, y, z, rx, ry, rz, *dynParams):
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
        print(string)
        return self.sendRecvMsg(string)

    def JointMovJ(self, j1, j2, j3, j4, j5, j6, *dynParams):
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
        return self.sendRecvMsg(string)

    def Jump(self):
        print("待定")

    def RelMovJ(self, offset1, offset2, offset3, offset4, offset5, offset6, *dynParams):
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
        return self.sendRecvMsg(string)

    def RelMovL(self, offsetX, offsetY, offsetZ, *dynParams):
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
        return self.sendRecvMsg(string)

    def MovLIO(self, x, y, z, a, b, c, *dynParams):
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
        return self.sendRecvMsg(string)

    def MovJIO(self, x, y, z, a, b, c, *dynParams):
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
        self.log("Send to 192.168.5.1:29999:" + string)
        for params in dynParams:
            string = string + "," + str(params)
        string = string + ")"
        return self.sendRecvMsg(string)

    def Arc(self, x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, *dynParams):
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
        return self.sendRecvMsg(string)

    def Circle3(
        self, x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, count, *dynParams
    ):
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
        return self.sendRecvMsg(string)

    def ServoJ(self, j1, j2, j3, j4, j5, j6, t=0.1, lookahead_time=50, gain=500):
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
        return self.sendRecvMsg(string)

    def ServoJS(self, j1, j2, j3, j4, j5, j6):
        """
        功能:基于关节空间的动态跟随运动。
        格式:ServoJS(J1,J2,J3,J4,J5,J6)
        """
        string = "ServoJS({:f},{:f},{:f},{:f},{:f},{:f})".format(j1, j2, j3, j4, j5, j6)
        return self.sendRecvMsg(string)

    def ServoP(self, x, y, z, a, b, c):
        """
        Dynamic following command based on Cartesian space
        x, y, z, a, b, c :Cartesian coordinate point value
        """
        string = "ServoP({:f},{:f},{:f},{:f},{:f},{:f})".format(x, y, z, a, b, c)
        return self.sendRecvMsg(string)

    def MoveJog(self, axis_id, *dynParams):
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
        return self.sendRecvMsg(string)

    def StartTrace(self, trace_name):
        """
        Trajectory fitting (track file Cartesian points)
        trace_name: track file name (including suffix)
        (The track path is stored in /dobot/userdata/project/process/trajectory/)

        It needs to be used together with `GetTraceStartPose(recv_string.json)` interface
        """
        string = f"StartTrace({trace_name})"
        return self.sendRecvMsg(string)

    def StartPath(self, trace_name, const, cart):
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
        return self.sendRecvMsg(string)

    def StartFCTrace(self, trace_name):
        """
        Trajectory fitting with force control. (track file Cartesian points)
        trace_name: track file name (including suffix)
        (The track path is stored in /dobot/userdata/project/process/trajectory/)

        It needs to be used together with `GetTraceStartPose(recv_string.json)` interface
        """
        string = f"StartFCTrace({trace_name})"
        return self.sendRecvMsg(string)

    def Sync(self):
        """
        The blocking program executes the queue instruction and returns after all the queue instructions are executed
        """
        string = "Sync()"
        return self.sendRecvMsg(string)

    def RelMovJTool(
        self,
        offset_x,
        offset_y,
        offset_z,
        offset_rx,
        offset_ry,
        offset_rz,
        tool,
        *dynParams,
    ):
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
            print(type(params), params)
            string = string + ", SpeedJ={:d}, AccJ={:d}, User={:d}".format(
                params[0], params[1], params[2]
            )
        string = string + ")"
        return self.sendRecvMsg(string)

    def RelMovLTool(
        self,
        offset_x,
        offset_y,
        offset_z,
        offset_rx,
        offset_ry,
        offset_rz,
        tool,
        *dynParams,
    ):
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
            print(type(params), params)
            string = string + ", SpeedJ={:d}, AccJ={:d}, User={:d}".format(
                params[0], params[1], params[2]
            )
        string = string + ")"
        return self.sendRecvMsg(string)

    def RelMovJUser(
        self,
        offset_x,
        offset_y,
        offset_z,
        offset_rx,
        offset_ry,
        offset_rz,
        user,
        *dynParams,
    ):
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
        return self.sendRecvMsg(string)

    def RelMovLUser(
        self,
        offset_x,
        offset_y,
        offset_z,
        offset_rx,
        offset_ry,
        offset_rz,
        user,
        *dynParams,
    ):
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
        return self.sendRecvMsg(string)

    def RelJointMovJ(
        self, offset1, offset2, offset3, offset4, offset5, offset6, *dynParams
    ):
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
        return self.sendRecvMsg(string)
