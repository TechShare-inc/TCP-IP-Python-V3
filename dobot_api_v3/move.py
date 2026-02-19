"""Movement commands for Dobot API (DobotApiMove class)."""

from __future__ import annotations

from loguru import logger

from .base import DobotApi
from .utils import DynParam, ToolDynParam, deprecated_alias


class DobotApiMove(DobotApi):
    """Movement command client for Dobot motion APIs.

    This class sends trajectory and servo commands to the move TCP port
    (usually ``30003``).
    """

    # ------------------------------------------------------------------
    # Protocol command methods (snake_case — primary implementation).
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
            >>> move.mov_j(200, 0, 200, 0, 0, 0)
            >>> move.mov_j(220, 20, 180, 0, 0, 0, "SpeedJ=40", "AccJ=40")
        """
        string = "MovJ({:f},{:f},{:f},{:f},{:f},{:f}".format(x, y, z, rx, ry, rz)
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        logger.debug(f"MovJ command: {string}")
        return self.send_recv_msg(string)

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
            >>> move.mov_l(250, 0, 180, 0, 0, 0)
            >>> move.mov_l(250, 30, 180, 0, 0, 0, "SpeedL=30", "AccL=30")
        """
        string = "MovL({:f},{:f},{:f},{:f},{:f},{:f}".format(x, y, z, rx, ry, rz)
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        logger.debug(f"MovL command: {string}")
        return self.send_recv_msg(string)

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
        """
        string = "JointMovJ({:f},{:f},{:f},{:f},{:f},{:f}".format(
            j1, j2, j3, j4, j5, j6
        )
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def jump(self) -> None:
        """Placeholder for Jump command.

        This method is intentionally not implemented in the current version.
        """
        logger.warning("TODO: Jump method not yet implemented.")

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
        """
        string = "RelMovJ({:f},{:f},{:f},{:f},{:f},{:f}".format(
            offset1, offset2, offset3, offset4, offset5, offset6
        )
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def rel_mov_l(
        self, offset_x: float, offset_y: float, offset_z: float, *dyn_params: DynParam
    ) -> str:
        """Relative Cartesian offset motion (linear mode).

        Args:
            offset_x: X-axis offset.
            offset_y: Y-axis offset.
            offset_z: Z-axis offset.
            *dyn_params: Optional motion parameters.

        Returns:
            Robot response string.
        """
        string = "RelMovL({:f},{:f},{:f}".format(offset_x, offset_y, offset_z)
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def mov_l_io(
        self,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
        *dyn_params: DynParam,
    ) -> str:
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
            Robot response string.
        """
        string = "MovLIO({:f},{:f},{:f},{:f},{:f},{:f}".format(x, y, z, a, b, c)
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def mov_j_io(
        self,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
        *dyn_params: DynParam,
    ) -> str:
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
            Robot response string.
        """
        string = "MovJIO({:f},{:f},{:f},{:f},{:f},{:f}".format(x, y, z, a, b, c)
        logger.debug(f"MovJIO command: {string}")
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

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
        string = (
            "Arc({:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f}".format(
                x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2
            )
        )
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def circle3(
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
        *dyn_params: DynParam,
    ) -> str:
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
            Robot response string.
        """
        string = "Circle3({:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:d}".format(
            x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, count
        )
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

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
        string = "ServoJ({:f},{:f},{:f},{:f},{:f},{:f},t={:f},lookahead_time={:f},gain={:f})".format(
            j1, j2, j3, j4, j5, j6, t, lookahead_time, gain
        )
        return self.send_recv_msg(string)

    def servo_js(
        self, j1: float, j2: float, j3: float, j4: float, j5: float, j6: float
    ) -> str:
        """Dynamic following in joint space (simplified form).

        Args:
            j1: Target joint 1 angle.
            j2: Target joint 2 angle.
            j3: Target joint 3 angle.
            j4: Target joint 4 angle.
            j5: Target joint 5 angle.
            j6: Target joint 6 angle.

        Returns:
            Robot response string.
        """
        string = "ServoJS({:f},{:f},{:f},{:f},{:f},{:f})".format(j1, j2, j3, j4, j5, j6)
        return self.send_recv_msg(string)

    def servo_p(
        self, x: float, y: float, z: float, a: float, b: float, c: float
    ) -> str:
        """Dynamic following in Cartesian space.

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
        string = "ServoP({:f},{:f},{:f},{:f},{:f},{:f})".format(x, y, z, a, b, c)
        return self.send_recv_msg(string)

    def move_jog(self, axis_id: str, *dyn_params: DynParam) -> str:
        """Jog motion along a single axis.

        Args:
            axis_id: Axis command such as ``"J1+"`` or ``"X-"``.
            *dyn_params: Optional jog parameters ``(coord_type, user, tool)``.

        Returns:
            Robot response string.

        Example:
            >>> move.move_jog("J1+")
            >>> move.move_jog("")
        """
        string = "MoveJog({:s}".format(axis_id)
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def start_trace(self, trace_name: str) -> str:
        """Execute a trajectory file (Cartesian points).

        Args:
            trace_name: Trajectory file name including suffix.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg(f"StartTrace({trace_name})")

    def start_path(self, trace_name: str, const: int, cart: int) -> str:
        """Replay a trajectory file (joint points).

        Args:
            trace_name: Trajectory file name including suffix.
            const: Constant-speed mode flag.
            cart: Cartesian/joint path flag.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg(f"StartPath({trace_name}, {const}, {cart})")

    def start_fc_trace(self, trace_name: str) -> str:
        """Execute a trajectory file with force control (Cartesian points).

        Args:
            trace_name: Trajectory file name including suffix.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg(f"StartFCTrace({trace_name})")

    def sync(self) -> str:
        """Block until all queued commands have been executed.

        Returns:
            Robot response string.

        Example:
            >>> move.mov_j(200, 0, 200, 0, 0, 0)
            >>> move.mov_l(220, 20, 180, 0, 0, 0)
            >>> move.sync()
        """
        return self.send_recv_msg("Sync()")

    def rel_mov_j_tool(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        tool: int,
        *dyn_params: ToolDynParam,
    ) -> str:
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
            Robot response string.
        """
        string = "RelMovJTool({:f},{:f},{:f},{:f},{:f},{:f}, {:d}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, tool
        )
        for params in dyn_params:
            logger.debug(f"RelMovJTool params: type={type(params)}, value={params}")
            string = string + ", SpeedJ={:d}, AccJ={:d}, User={:d}".format(
                params[0], params[1], params[2]
            )
        string = string + ")"
        return self.send_recv_msg(string)

    def rel_mov_l_tool(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        tool: int,
        *dyn_params: ToolDynParam,
    ) -> str:
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
            Robot response string.
        """
        string = "RelMovLTool({:f},{:f},{:f},{:f},{:f},{:f}, {:d}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, tool
        )
        for params in dyn_params:
            logger.debug(f"RelMovLTool params: type={type(params)}, value={params}")
            string = string + ", SpeedJ={:d}, AccJ={:d}, User={:d}".format(
                params[0], params[1], params[2]
            )
        string = string + ")"
        return self.send_recv_msg(string)

    def rel_mov_j_user(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        user: int,
        *dyn_params: DynParam,
    ) -> str:
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
            Robot response string.
        """
        string = "RelMovJUser({:f},{:f},{:f},{:f},{:f},{:f}, {:d}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, user
        )
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def rel_mov_l_user(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        user: int,
        *dyn_params: DynParam,
    ) -> str:
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
            Robot response string.
        """
        string = "RelMovLUser({:f},{:f},{:f},{:f},{:f},{:f}, {:d}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, user
        )
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def rel_joint_mov_j(
        self,
        offset1: float,
        offset2: float,
        offset3: float,
        offset4: float,
        offset5: float,
        offset6: float,
        *dyn_params: DynParam,
    ) -> str:
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
            Robot response string.
        """
        string = "RelJointMovJ({:f},{:f},{:f},{:f},{:f},{:f}".format(
            offset1, offset2, offset3, offset4, offset5, offset6
        )
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    # ------------------------------------------------------------------
    # Deprecated PascalCase aliases — do not use in new code.
    # ------------------------------------------------------------------

    @deprecated_alias("mov_j")
    def MovJ(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.mov_j(*args, **kwargs)

    @deprecated_alias("mov_l")
    def MovL(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.mov_l(*args, **kwargs)

    @deprecated_alias("joint_mov_j")
    def JointMovJ(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.joint_mov_j(*args, **kwargs)

    @deprecated_alias("jump")
    def Jump(self) -> None:
        return self.jump()

    @deprecated_alias("rel_mov_j")
    def RelMovJ(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.rel_mov_j(*args, **kwargs)

    @deprecated_alias("rel_mov_l")
    def RelMovL(
        self, offsetX: float, offsetY: float, offsetZ: float, *dyn_params: DynParam
    ) -> str:
        return self.rel_mov_l(offsetX, offsetY, offsetZ, *dyn_params)

    @deprecated_alias("mov_l_io")
    def MovLIO(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.mov_l_io(*args, **kwargs)

    @deprecated_alias("mov_j_io")
    def MovJIO(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.mov_j_io(*args, **kwargs)

    @deprecated_alias("arc")
    def Arc(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.arc(*args, **kwargs)

    @deprecated_alias("circle3")
    def Circle3(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.circle3(*args, **kwargs)

    @deprecated_alias("servo_j")
    def ServoJ(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.servo_j(*args, **kwargs)

    @deprecated_alias("servo_js")
    def ServoJS(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.servo_js(*args, **kwargs)

    @deprecated_alias("servo_p")
    def ServoP(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.servo_p(*args, **kwargs)

    @deprecated_alias("move_jog")
    def MoveJog(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.move_jog(*args, **kwargs)

    @deprecated_alias("start_trace")
    def StartTrace(self, trace_name: str) -> str:
        return self.start_trace(trace_name)

    @deprecated_alias("start_path")
    def StartPath(self, trace_name: str, const: int, cart: int) -> str:
        return self.start_path(trace_name, const, cart)

    @deprecated_alias("start_fc_trace")
    def StartFCTrace(self, trace_name: str) -> str:
        return self.start_fc_trace(trace_name)

    @deprecated_alias("sync")
    def Sync(self) -> str:
        return self.sync()

    @deprecated_alias("rel_mov_j_tool")
    def RelMovJTool(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.rel_mov_j_tool(*args, **kwargs)

    @deprecated_alias("rel_mov_l_tool")
    def RelMovLTool(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.rel_mov_l_tool(*args, **kwargs)

    @deprecated_alias("rel_mov_j_user")
    def RelMovJUser(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.rel_mov_j_user(*args, **kwargs)

    @deprecated_alias("rel_mov_l_user")
    def RelMovLUser(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.rel_mov_l_user(*args, **kwargs)

    @deprecated_alias("rel_joint_mov_j")
    def RelJointMovJ(self, *args, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self.rel_joint_mov_j(*args, **kwargs)
