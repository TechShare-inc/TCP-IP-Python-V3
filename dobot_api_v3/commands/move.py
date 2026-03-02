"""Movement commands for Dobot API (DobotApiMove class)."""

from __future__ import annotations

from loguru import logger

from ..base import DobotApi
from ..utils import DynParam, ToolDynParam
from ._serialization import _SerializationMixin


class DobotApiMove(_SerializationMixin, DobotApi):
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
    ) -> int:
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
        string = "MovJ({:f},{:f},{:f},{:f},{:f},{:f}".format(x, y, z, rx, ry, rz)
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        logger.debug(f"MovJ command: {string}")
        return self._recv_ack(string)

    def mov_l(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
        *dyn_params: DynParam,
    ) -> int:
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
        string = "MovL({:f},{:f},{:f},{:f},{:f},{:f}".format(x, y, z, rx, ry, rz)
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        logger.debug(f"MovL command: {string}")
        return self._recv_ack(string)

    def joint_mov_j(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        *dyn_params: DynParam,
    ) -> int:
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
        string = "JointMovJ({:f},{:f},{:f},{:f},{:f},{:f}".format(
            j1, j2, j3, j4, j5, j6
        )
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self._recv_ack(string)

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
    ) -> int:
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
        string = "RelMovJ({:f},{:f},{:f},{:f},{:f},{:f}".format(
            offset1, offset2, offset3, offset4, offset5, offset6
        )
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self._recv_ack(string)

    def rel_mov_l(
        self, offset_x: float, offset_y: float, offset_z: float, *dyn_params: DynParam
    ) -> int:
        """Relative Cartesian offset motion (linear mode).

        Args:
            offset_x: X-axis offset.
            offset_y: Y-axis offset.
            offset_z: Z-axis offset.
            *dyn_params: Optional motion parameters.

        Returns:
            Command queue ID.
        """
        string = "RelMovL({:f},{:f},{:f}".format(offset_x, offset_y, offset_z)
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self._recv_ack(string)

    def mov_l_io(
        self,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
        *dyn_params: DynParam,
    ) -> int:
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
        string = "MovLIO({:f},{:f},{:f},{:f},{:f},{:f}".format(x, y, z, a, b, c)
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self._recv_ack(string)

    def mov_j_io(
        self,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
        *dyn_params: DynParam,
    ) -> int:
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
        string = "MovJIO({:f},{:f},{:f},{:f},{:f},{:f}".format(x, y, z, a, b, c)
        logger.debug(f"MovJIO command: {string}")
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self._recv_ack(string)

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
    ) -> int:
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
        string = (
            "Arc({:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f}".format(
                x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2
            )
        )
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self._recv_ack(string)

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
    ) -> int:
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
        string = "Circle3({:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:d}".format(
            x1, y1, z1, a1, b1, c1, x2, y2, z2, a2, b2, c2, count
        )
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self._recv_ack(string)

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
    ) -> int:
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
        string = "ServoJ({:f},{:f},{:f},{:f},{:f},{:f},t={:f},lookahead_time={:f},gain={:f})".format(
            j1, j2, j3, j4, j5, j6, t, lookahead_time, gain
        )
        return self._recv_ack(string)

    def servo_js(
        self, j1: float, j2: float, j3: float, j4: float, j5: float, j6: float
    ) -> int:
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
        string = "ServoJS({:f},{:f},{:f},{:f},{:f},{:f})".format(j1, j2, j3, j4, j5, j6)
        return self._recv_ack(string)

    def servo_p(
        self, x: float, y: float, z: float, a: float, b: float, c: float
    ) -> int:
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
        string = "ServoP({:f},{:f},{:f},{:f},{:f},{:f})".format(x, y, z, a, b, c)
        return self._recv_ack(string)

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
        string = "MoveJog({:s}".format(axis_id)
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self._recv_ack(string)

    def start_trace(self, trace_name: str) -> int:
        """Execute a trajectory file (Cartesian points).

        Args:
            trace_name: Trajectory file name including suffix.

        Returns:
            Command queue ID.
        """
        return self._recv_ack(f"StartTrace({trace_name})")

    def start_path(self, trace_name: str, const: int, cart: int) -> int:
        """Replay a trajectory file (joint points).

        Args:
            trace_name: Trajectory file name including suffix.
            const: Constant-speed mode flag.
            cart: Cartesian/joint path flag.

        Returns:
            Command queue ID.
        """
        return self._recv_ack(f"StartPath({trace_name}, {const}, {cart})")

    def start_fc_trace(self, trace_name: str) -> int:
        """Execute a trajectory file with force control (Cartesian points).

        Args:
            trace_name: Trajectory file name including suffix.

        Returns:
            Command queue ID.
        """
        return self._recv_ack(f"StartFCTrace({trace_name})")

    def sync(self) -> int:
        """Block until all queued commands have been executed.

        Returns:
            Command queue ID.

        Example:
            >>> move.mov_j(200, 0, 200, 0, 0, 0)
            >>> move.mov_l(220, 20, 180, 0, 0, 0)
            >>> move.sync()
        """
        return self._recv_ack("Sync()")

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
    ) -> int:
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
        string = "RelMovJTool({:f},{:f},{:f},{:f},{:f},{:f}, {:d}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, tool
        )
        for params in dyn_params:
            logger.debug(f"RelMovJTool params: type={type(params)}, value={params}")
            string = string + ", SpeedJ={:d}, AccJ={:d}, User={:d}".format(
                params[0], params[1], params[2]
            )
        string = string + ")"
        return self._recv_ack(string)

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
    ) -> int:
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
        string = "RelMovLTool({:f},{:f},{:f},{:f},{:f},{:f}, {:d}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, tool
        )
        for params in dyn_params:
            logger.debug(f"RelMovLTool params: type={type(params)}, value={params}")
            string = string + ", SpeedJ={:d}, AccJ={:d}, User={:d}".format(
                params[0], params[1], params[2]
            )
        string = string + ")"
        return self._recv_ack(string)

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
    ) -> int:
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
        string = "RelMovJUser({:f},{:f},{:f},{:f},{:f},{:f}, {:d}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, user
        )
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self._recv_ack(string)

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
    ) -> int:
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
        string = "RelMovLUser({:f},{:f},{:f},{:f},{:f},{:f}, {:d}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz, user
        )
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self._recv_ack(string)

    def rel_joint_mov_j(
        self,
        offset1: float,
        offset2: float,
        offset3: float,
        offset4: float,
        offset5: float,
        offset6: float,
        *dyn_params: DynParam,
    ) -> int:
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
        string = "RelJointMovJ({:f},{:f},{:f},{:f},{:f},{:f}".format(
            offset1, offset2, offset3, offset4, offset5, offset6
        )
        for params in dyn_params:
            string = string + "," + str(params)
        string = string + ")"
        return self._recv_ack(string)
