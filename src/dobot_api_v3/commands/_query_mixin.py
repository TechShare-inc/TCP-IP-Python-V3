"""Query, safety, drag, trajectory, and terminal command mixin for DobotApiDashboard."""

from __future__ import annotations

from loguru import logger

from ..utils import DynParam, Pose
from ._serialization import _SerializationMixin


class _QueryMixin(_SerializationMixin):
    """State query, safety, drag mode, trajectory, and terminal configuration commands."""

    def get_angle(self) -> Pose:
        """Get current joint angles.

        Returns:
            Joint angles as ``(j1, j2, j3, j4, j5, j6)``.
        """
        return self._recv_pose("GetAngle()")

    def get_pose(self) -> Pose:
        """Get current Cartesian pose.

        Returns:
            Cartesian pose as ``(x, y, z, rx, ry, rz)``.
        """
        return self._recv_pose("GetPose()")

    def get_error_id(self) -> tuple[int, ...]:
        """Get robot error code.

        Returns:
            Tuple of non-zero alarm codes (may be empty).
        """
        return self._recv_error_ids("GetErrorID()")

    def positive_solution(
        self,
        offset1: float,
        offset2: float,
        offset3: float,
        offset4: float,
        offset5: float,
        offset6: float,
        user: int,
        tool: int,
    ) -> Pose:
        """Run forward kinematics from joint angles to Cartesian pose.

        Args:
            offset1: Joint 1 angle.
            offset2: Joint 2 angle.
            offset3: Joint 3 angle.
            offset4: Joint 4 angle.
            offset5: Joint 5 angle.
            offset6: Joint 6 angle.
            user: User coordinate index.
            tool: Tool coordinate index.

        Returns:
            Cartesian pose as ``(x, y, z, rx, ry, rz)``.
        """
        string = (
            "PositiveSolution({:f},{:f},{:f},{:f},{:f},{:f},{:d},{:d}".format(
                offset1, offset2, offset3, offset4, offset5, offset6, user, tool
            )
            + ")"
        )
        return self._recv_pose(string)

    def inverse_solution(
        self,
        offset1: float,
        offset2: float,
        offset3: float,
        offset4: float,
        offset5: float,
        offset6: float,
        user: int,
        tool: int,
        *dyn_params: DynParam,
    ) -> Pose:  # noqa: F821
        """Run inverse kinematics from Cartesian pose to joint angles.

        Args:
            offset1: X position.
            offset2: Y position.
            offset3: Z position.
            offset4: RX rotation.
            offset5: RY rotation.
            offset6: RZ rotation.
            user: User coordinate index.
            tool: Tool coordinate index.
            *dyn_params: Optional solver parameters.

        Returns:
            Joint angles as ``(j1, j2, j3, j4, j5, j6)``.
        """
        string = "InverseSolution({:f},{:f},{:f},{:f},{:f},{:f},{:d},{:d}".format(
            offset1, offset2, offset3, offset4, offset5, offset6, user, tool
        )
        for params in dyn_params:
            logger.debug(f"InverseSolution params: type={type(params)}, value={params}")
            string = string + repr(params)
        string = string + ")"
        return self._recv_pose(string)

    def get_six_force_data(self) -> Pose:
        """Read six-axis force sensor data.

        Returns:
            Force/torque values as ``(fx, fy, fz, mx, my, mz)``.
        """
        return self._recv_pose("GetSixForceData()")

    def get_trace_start_pose(self, offset1: str) -> Pose:
        """Get starting pose of a Cartesian trajectory file.

        Args:
            offset1: Trajectory file name.

        Returns:
            Starting pose as ``(x, y, z, rx, ry, rz)``.
        """
        return self._recv_pose("GetTraceStartPose({:s})".format(offset1))

    def get_path_start_pose(self, offset1: str) -> Pose:
        """Get starting pose of a joint path file.

        Args:
            offset1: Path file name.

        Returns:
            Starting pose as ``(x, y, z, rx, ry, rz)``.
        """
        return self._recv_pose("GetPathStartPose({:s})".format(offset1))

    def set_safe_skin(self, offset1: int) -> int:
        """Configure safe-skin feature.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("SetSafeSkin({:d})".format(offset1))

    def set_obstacle_avoid(self, offset1: int) -> int:
        """Configure obstacle avoidance feature.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("SetObstacleAvoid({:d})".format(offset1))

    def set_collide_drag(self, offset1: int) -> int:
        """Configure collision drag mode.

        Args:
            offset1: Drag mode flag.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("SetCollideDrag({:d})".format(offset1))

    def start_drag(self) -> int:
        """Enable drag mode.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("StartDrag()")

    def stop_drag(self) -> int:
        """Disable drag mode.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("StopDrag()")

    def brake_control(self, offset1: int, offset2: int) -> int:
        """Control joint brakes.

        Args:
            offset1: Joint index.
            offset2: Brake control value.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("BrakeControl({:d},{:d})".format(offset1, offset2))

    def handle_traj_points(self, offset1: str) -> int:
        """Process a trajectory points file.

        Args:
            offset1: Trajectory file name.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("HandleTrajPoints({:s})".format(offset1))

    def tcp_speed(self, offset1: int) -> int:
        """Set TCP speed.

        Args:
            offset1: TCP speed value.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("TCPSpeed({:d})".format(offset1))

    def tcp_speed_end(self) -> int:
        """End TCP speed mode.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("TCPSpeedEnd()")

    def set_terminal_keys(self, offset1: int) -> int:
        """Configure terminal key behavior.

        Args:
            offset1: Key mode value.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("SetTerminalKeys({:d})".format(offset1))

    def set_terminal_485(
        self, offset1: int, offset2: int, offset3: str, offset4: int
    ) -> int:
        """Set terminal RS-485 parameters.

        Args:
            offset1: Baud rate.
            offset2: Data bits.
            offset3: Parity setting.
            offset4: Stop bits.

        Returns:
            Command queue ID.
        """
        return self._recv_ack(
            "SetTerminal485({:d},{:d},{:s},{:d})".format(
                offset1, offset2, offset3, offset4
            )
        )

    def get_terminal_485(self) -> tuple[str, ...]:
        """Get terminal RS-485 configuration.

        Returns:
            Tuple of configuration tokens (baud, data bits, parity, stop bits).
        """
        return self._recv_str_list("GetTerminal485()")
