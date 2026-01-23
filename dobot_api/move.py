"""Motion API for Dobot robot movement commands."""

from __future__ import annotations
from typing import overload

from dobot_api.base import DobotApi


class DobotApiMove(DobotApi):
    """Motion API for robot movement commands.

    This class provides motion commands including joint motion (MovJ),
    linear motion (MovL), servo control, jogging, and trajectory execution.
    All commands are sent through port 30003.

    Example:
        move = DobotApiMove("192.168.1.6", 30003)
        move.MovJ(300, 0, 200, 0, 0, 0)
        move.MovL(350, 50, 200, 0, 0, 0)

    """

    # ==================== Point-to-Point Motion ====================

    def MovJ(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
        *dynParams,
    ) -> str:
        """Joint motion (point-to-point).

        Args:
            x: X coordinate in Cartesian system
            y: Y coordinate in Cartesian system
            z: Z coordinate in Cartesian system
            rx: Rx axis rotation
            ry: Ry axis rotation
            rz: Rz axis rotation
            *dynParams: Additional parameters (User, Tool, SpeedJ, AccJ, etc.)

        Returns:
            Response string from robot

        """
        cmd = f"MovJ({x:f},{y:f},{z:f},{rx:f},{ry:f},{rz:f}"
        for param in dynParams:
            cmd += f",{param}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    def JointMovJ(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        *dynParams,
    ) -> str:
        """Joint motion using joint coordinates.

        Args:
            j1-j6: Joint angle values
            *dynParams: Additional parameters

        Returns:
            Response string from robot

        """
        cmd = f"JointMovJ({j1:f},{j2:f},{j3:f},{j4:f},{j5:f},{j6:f}"
        for param in dynParams:
            cmd += f",{param}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    # ==================== Linear Motion ====================

    def MovL(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
        *dynParams,
    ) -> str:
        """Linear motion.

        Args:
            x: X coordinate in Cartesian system
            y: Y coordinate in Cartesian system
            z: Z coordinate in Cartesian system
            rx: Rx axis rotation
            ry: Ry axis rotation
            rz: Rz axis rotation
            *dynParams: Additional parameters

        Returns:
            Response string from robot

        """
        cmd = f"MovL({x:f},{y:f},{z:f},{rx:f},{ry:f},{rz:f}"
        for param in dynParams:
            cmd += f",{param}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    # ==================== Relative Motion ====================

    def RelMovJ(
        self,
        dx: float,
        dy: float,
        dz: float,
        drx: float,
        dry: float,
        drz: float,
        *dynParams,
    ) -> str:
        """Relative joint motion (offset from current position).

        Args:
            dx-drz: Offset values
            *dynParams: Additional parameters

        """
        cmd = f"RelMovJ({dx:f},{dy:f},{dz:f},{drx:f},{dry:f},{drz:f}"
        for param in dynParams:
            cmd += f",{param}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    def RelMovL(self, offsetX: float, offsetY: float, offsetZ: float, *dynParams) -> str:
        """Relative linear motion.

        Args:
            offsetX: X-axis offset
            offsetY: Y-axis offset
            offsetZ: Z-axis offset
            *dynParams: Additional parameters

        """
        cmd = f"RelMovL({offsetX:f},{offsetY:f},{offsetZ:f}"
        for param in dynParams:
            cmd += f",{param}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    def RelMovJTool(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        tool: int,
        *dynParams,
    ) -> str:
        """Relative joint motion along tool coordinate system.

        Args:
            offset_x-offset_rz: Offset values
            tool: Tool coordinate system index (0-9)
            *dynParams: (speed_j, acc_j, user) tuple

        """
        cmd = f"RelMovJTool({offset_x:f},{offset_y:f},{offset_z:f},{offset_rx:f},{offset_ry:f},{offset_rz:f},{tool:d}"
        for param in dynParams:
            cmd += f", SpeedJ={param[0]:d}, AccJ={param[1]:d}, User={param[2]:d}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    def RelMovLTool(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        tool: int,
        *dynParams,
    ) -> str:
        """Relative linear motion along tool coordinate system.

        Args:
            offset_x-offset_rz: Offset values
            tool: Tool coordinate system index (0-9)
            *dynParams: (speed_l, acc_l, user) tuple

        """
        cmd = f"RelMovLTool({offset_x:f},{offset_y:f},{offset_z:f},{offset_rx:f},{offset_ry:f},{offset_rz:f},{tool:d}"
        for param in dynParams:
            cmd += f", SpeedJ={param[0]:d}, AccJ={param[1]:d}, User={param[2]:d}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    def RelMovJUser(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        user: int,
        *dynParams,
    ) -> str:
        """Relative joint motion along user coordinate system.

        Args:
            offset_x-offset_rz: Offset values
            user: User coordinate system index (0-9)
            *dynParams: Additional parameters

        """
        cmd = f"RelMovJUser({offset_x:f},{offset_y:f},{offset_z:f},{offset_rx:f},{offset_ry:f},{offset_rz:f},{user:d}"
        for param in dynParams:
            cmd += f",{param}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    def RelMovLUser(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        user: int,
        *dynParams,
    ) -> str:
        """Relative linear motion along user coordinate system.

        Args:
            offset_x-offset_rz: Offset values
            user: User coordinate system index (0-9)
            *dynParams: Additional parameters

        """
        cmd = f"RelMovLUser({offset_x:f},{offset_y:f},{offset_z:f},{offset_rx:f},{offset_ry:f},{offset_rz:f},{user:d}"
        for param in dynParams:
            cmd += f",{param}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    def RelJointMovJ(
        self,
        dj1: float,
        dj2: float,
        dj3: float,
        dj4: float,
        dj5: float,
        dj6: float,
        *dynParams,
    ) -> str:
        """Relative joint motion in joint space.

        Args:
            dj1-dj6: Joint offset values
            *dynParams: Additional parameters

        """
        cmd = f"RelJointMovJ({dj1:f},{dj2:f},{dj3:f},{dj4:f},{dj5:f},{dj6:f}"
        for param in dynParams:
            cmd += f",{param}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    # ==================== Motion with I/O ====================

    def MovLIO(
        self,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
        *dynParams,
    ) -> str:
        """Linear motion with parallel digital output control.

        Args:
            x, y, z, a, b, c: Target pose
            *dynParams: I/O settings as tuples (Mode, Distance, Index, Status)
                Mode: 0=percentage, 1=distance from start/end
                Distance: If Mode=0, range 0-100; If Mode=1, positive=from start, negative=from end
                Index: Digital output index (1-24)
                Status: Output state (0/1)

        Example:
            move.MovLIO(0, 50, 0, 0, 0, 0, (0, 50, 1, 0), (1, 1, 2, 1))

        """
        cmd = f"MovLIO({x:f},{y:f},{z:f},{a:f},{b:f},{c:f}"
        for param in dynParams:
            cmd += f",{param}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    def MovJIO(
        self,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
        *dynParams,
    ) -> str:
        """Point-to-point motion with parallel digital output control.

        Args:
            x, y, z, a, b, c: Target pose
            *dynParams: I/O settings (same as MovLIO)

        Example:
            move.MovJIO(0, 50, 0, 0, 0, 0, (0, 50, 1, 0), (1, 1, 2, 1))

        """
        cmd = f"MovJIO({x:f},{y:f},{z:f},{a:f},{b:f},{c:f}"
        for param in dynParams:
            cmd += f",{param}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    # ==================== Arc & Circle Motion ====================

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
        *dynParams,
    ) -> str:
        """Arc motion through intermediate point to end point.

        Args:
            x1, y1, z1, a1, b1, c1: Intermediate point coordinates
            x2, y2, z2, a2, b2, c2: End point coordinates
            *dynParams: Additional parameters

        Note: Should be used with other motion commands.

        """
        cmd = f"Arc({x1:f},{y1:f},{z1:f},{a1:f},{b1:f},{c1:f},{x2:f},{y2:f},{z2:f},{a2:f},{b2:f},{c2:f}"
        for param in dynParams:
            cmd += f",{param}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

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
        *dynParams,
    ) -> str:
        """Full circle motion.

        Args:
            x1, y1, z1, a1, b1, c1: Intermediate point coordinates
            x2, y2, z2, a2, b2, c2: End point coordinates
            count: Number of laps
            *dynParams: Additional parameters

        Note: Should be used with other motion commands.

        """
        cmd = f"Circle3({x1:f},{y1:f},{z1:f},{a1:f},{b1:f},{c1:f},{x2:f},{y2:f},{z2:f},{a2:f},{b2:f},{c2:f},{count:d}"
        for param in dynParams:
            cmd += f",{param}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    # ==================== Servo Control ====================

    @overload
    def ServoJ(
        self,
        joint_angles: list[float],
        t: float = 0.1,
        lookahead_time: float = 50,
        gain: float = 500,
    ) -> str: ...

    @overload
    def ServoJ(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        t: float = 0.1,
        lookahead_time: float = 50,
        gain: float = 500,
    ) -> str: ...

    def ServoJ(self, *args, **kwargs) -> str:
        """Dynamic servo control in joint space.

        Args:
            j1-j6: Joint position values
            t: Execution time for this point (0.02-3600.0 seconds, default 0.1)
            lookahead_time: Similar to PID D-term (20.0-100.0, default 50)
            gain: Position proportional gain, similar to PID P-term (200.0-1000.0, default 500)

        """
        cmd = "ServoJ("

        if len(args) == 1 and isinstance(args[0], list):
            cmd += ",".join(f"{angle:f}" for angle in args[0])
        else:
            cmd += ",".join(f"{arg:f}" for arg in args)
        cmd += f",{kwargs.get('t', 0.1):f},{kwargs.get('lookahead_time', 50):f},{kwargs.get('gain', 500):f})"

        return self.sendRecvMsg(cmd)

    @overload
    def ServoJS(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
    ) -> str: ...

    @overload
    def ServoJS(self, joint_angles: list[float]) -> str: ...

    def ServoJS(self, *args, **kwargs) -> str:
        """Dynamic servo control in joint space (simple version).

        Args:
            j1-j6: Joint position values, or
            joint_angles: List of joint angle values

        """
        if len(args) == 1 and isinstance(args[0], list):
            cmd = f"ServoJS({','.join(f'{angle:f}' for angle in args[0])})"
        else:
            cmd = f"ServoJS({','.join(f'{arg:f}' for arg in args)})"
        return self.sendRecvMsg(cmd)

    def ServoP(
        self,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
    ) -> str:
        """Dynamic servo control in Cartesian space.

        Args:
            x, y, z, a, b, c: Cartesian coordinate point values

        """
        cmd = f"ServoP({x:f},{y:f},{z:f},{a:f},{b:f},{c:f})"
        return self.sendRecvMsg(cmd)

    # ==================== Jog Control ====================

    def MoveJog(self, axis_id: str, *dynParams) -> str:
        """Jog motion control.

        Args:
            axis_id: Axis to jog, one of:
                - Joint: J1+, J1-, J2+, J2-, J3+, J3-, J4+, J4-, J5+, J5-, J6+, J6-
                - Cartesian: X+, X-, Y+, Y-, Z+, Z-, Rx+, Rx-, Ry+, Ry-, Rz+, Rz-
            *dynParams: (coord_type, user_index, tool_index)
                coord_type: 1=user coordinate, 2=tool coordinate (default 1)
                user_index: User index 0-9 (default 0)
                tool_index: Tool index 0-9 (default 0)

        """
        cmd = f"MoveJog({axis_id}"
        for param in dynParams:
            cmd += f",{param}"
        cmd += ")"
        return self.sendRecvMsg(cmd)

    # ==================== Trajectory ====================

    def StartTrace(self, trace_name: str) -> str:
        """Start trajectory fitting (Cartesian points).

        Args:
            trace_name: Trajectory file name (including suffix)

        Note: Trajectory path is /dobot/userdata/project/process/trajectory/
              Use with GetTraceStartPose() interface.

        """
        return self.sendRecvMsg(f"StartTrace({trace_name})")

    def StartPath(self, trace_name: str, const: int, cart: int) -> str:
        """Start trajectory reproduction (joint points).

        Args:
            trace_name: Trajectory file name (including suffix)
            const: 1=constant speed (removes pauses), 0=original speed
            cart: 1=Cartesian path, 0=joint path

        Note: Trajectory path is /dobot/userdata/project/process/trajectory/
              Use with GetTraceStartPose() interface.

        """
        return self.sendRecvMsg(f"StartPath({trace_name},{const},{cart})")

    def StartFCTrace(self, trace_name: str) -> str:
        """Start trajectory fitting with force control.

        Args:
            trace_name: Trajectory file name (including suffix)

        Note: Use with GetTraceStartPose() interface.

        """
        return self.sendRecvMsg(f"StartFCTrace({trace_name})")

    # ==================== Synchronization ====================

    def Sync(self) -> str:
        """Block until all queued commands are executed.

        Returns after all queue instructions have been executed.
        """
        return self.sendRecvMsg("Sync()")
