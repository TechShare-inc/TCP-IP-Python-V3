"""Movement commands for Dobot API (DobotApiMove class)."""

from __future__ import annotations

from loguru import logger

from .base import DobotApi
from .utils import DynParam, ToolDynParam, deprecated_alias


class DobotApiMove(DobotApi):
    """Movement class for robot motion commands. Connects to move port (30003)."""

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

        x/y/z/rx/ry/rz: Target Cartesian pose
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

        x/y/z/rx/ry/rz: Target Cartesian pose
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

        j1–j6: Target joint angles
        """
        string = "JointMovJ({:f},{:f},{:f},{:f},{:f},{:f}".format(
            j1, j2, j3, j4, j5, j6
        )
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def jump(self) -> None:
        """TODO: Jump method not yet implemented."""
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

        offset1–offset6: Joint offset values
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

        offset_x/offset_y/offset_z: Cartesian offsets
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

        x/y/z/a/b/c: Target Cartesian pose
        *dyn_params: (Mode, Distance, Index, Status) tuples
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

        x/y/z/a/b/c: Target Cartesian pose
        *dyn_params: (Mode, Distance, Index, Status) tuples
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

        x1/y1/z1/a1/b1/c1: Intermediate point
        x2/y2/z2/a2/b2/c2: End point
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

        x1/y1/z1/a1/b1/c1: Intermediate point
        x2/y2/z2/a2/b2/c2: End point
        count: Number of full rotations
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

        j1–j6: Target joint angles
        t: Point run time in seconds (0.02–3600.0, default 0.1)
        lookahead_time: D-term equivalent (20.0–100.0, default 50.0)
        gain: P-term equivalent (200.0–1000.0, default 500.0)
        """
        string = "ServoJ({:f},{:f},{:f},{:f},{:f},{:f},t={:f},lookahead_time={:f},gain={:f})".format(
            j1, j2, j3, j4, j5, j6, t, lookahead_time, gain
        )
        return self.send_recv_msg(string)

    def servo_js(
        self, j1: float, j2: float, j3: float, j4: float, j5: float, j6: float
    ) -> str:
        """Dynamic following in joint space (simplified form).

        j1–j6: Target joint angles
        """
        string = "ServoJS({:f},{:f},{:f},{:f},{:f},{:f})".format(j1, j2, j3, j4, j5, j6)
        return self.send_recv_msg(string)

    def servo_p(
        self, x: float, y: float, z: float, a: float, b: float, c: float
    ) -> str:
        """Dynamic following in Cartesian space.

        x/y/z/a/b/c: Target Cartesian pose
        """
        string = "ServoP({:f},{:f},{:f},{:f},{:f},{:f})".format(x, y, z, a, b, c)
        return self.send_recv_msg(string)

    def move_jog(self, axis_id: str, *dyn_params: DynParam) -> str:
        """Jog motion along a single axis.

        axis_id: e.g. "J1+", "X-", "Rz+"
        *dyn_params: Optional (coord_type, user_index, tool_index)
        """
        string = "MoveJog({:s}".format(axis_id)
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def start_trace(self, trace_name: str) -> str:
        """Execute a trajectory file (Cartesian points).

        trace_name: File name including suffix (stored in
            /dobot/userdata/project/process/trajectory/)
        """
        return self.send_recv_msg(f"StartTrace({trace_name})")

    def start_path(self, trace_name: str, const: int, cart: int) -> str:
        """Replay a trajectory file (joint points).

        trace_name: File name including suffix
        const: 1 = constant speed (removes pause/dead zones); 0 = original speed
        cart: 1 = Cartesian path; 0 = joint path
        """
        return self.send_recv_msg(f"StartPath({trace_name}, {const}, {cart})")

    def start_fc_trace(self, trace_name: str) -> str:
        """Execute a trajectory file with force control (Cartesian points).

        trace_name: File name including suffix
        """
        return self.send_recv_msg(f"StartFCTrace({trace_name})")

    def sync(self) -> str:
        """Block until all queued commands have been executed."""
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

        offset_x/y/z/rx/ry/rz: Offsets in tool frame
        tool: Tool coordinate system index (0–9)
        *dyn_params: Optional (speed_j, acc_j, user) tuples
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

        offset_x/y/z/rx/ry/rz: Offsets in tool frame
        tool: Tool coordinate system index (0–9)
        *dyn_params: Optional (speed_l, acc_l, user) tuples
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

        offset_x/y/z/rx/ry/rz: Offsets in user frame
        user: User coordinate system index (0–9)
        *dyn_params: Optional (speed_j, acc_j, tool) tuples
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

        offset_x/y/z/rx/ry/rz: Offsets in user frame
        user: User coordinate system index (0–9)
        *dyn_params: Optional (speed_l, acc_l, tool) tuples
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

        offset1–offset6: Per-axis joint offsets
        *dyn_params: Optional (speed_j, acc_j) pairs
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
