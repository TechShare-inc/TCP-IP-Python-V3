"""Relative motion command mixin for DobotApiMove."""

from __future__ import annotations

from loguru import logger

from ..utils import DynParam, ToolDynParam
from ._serialization import _SerializationMixin


class _RelativeMotionMixin(_SerializationMixin):
    """Relative (offset-based) motion commands.

    Provides relative joint, Cartesian, tool-frame, and user-frame motion
    primitives.
    """

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
