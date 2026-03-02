"""Query, safety, drag, trajectory, and terminal command mixin for DobotApiDashboard."""

from __future__ import annotations

from loguru import logger

from ..utils import DynParam
from ._serialization import _SerializationMixin


class _QueryMixin(_SerializationMixin):
    """State query, safety, drag mode, trajectory, and terminal configuration commands."""

    def get_angle(self) -> str:
        """Get current joint angles."""
        return self.send_recv_msg("GetAngle()")

    def get_pose(self) -> str:
        """Get current Cartesian pose."""
        return self.send_recv_msg("GetPose()")

    def get_error_id(self) -> str:
        """Get robot error code."""
        return self.send_recv_msg("GetErrorID()")

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
    ) -> str:
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
            Robot response string.
        """
        string = (
            "PositiveSolution({:f},{:f},{:f},{:f},{:f},{:f},{:d},{:d}".format(
                offset1, offset2, offset3, offset4, offset5, offset6, user, tool
            )
            + ")"
        )
        return self.send_recv_msg(string)

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
    ) -> str:
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
            Robot response string.
        """
        string = "InverseSolution({:f},{:f},{:f},{:f},{:f},{:f},{:d},{:d}".format(
            offset1, offset2, offset3, offset4, offset5, offset6, user, tool
        )
        for params in dyn_params:
            logger.debug(f"InverseSolution params: type={type(params)}, value={params}")
            string = string + repr(params)
        string = string + ")"
        return self.send_recv_msg(string)

    def get_six_force_data(self) -> str:
        """Read six-axis force sensor data."""
        return self.send_recv_msg("GetSixForceData()")

    def get_trace_start_pose(self, offset1: str) -> str:
        """Get starting pose of a Cartesian trajectory file.

        Args:
            offset1: Trajectory file name.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("GetTraceStartPose({:s})".format(offset1))

    def get_path_start_pose(self, offset1: str) -> str:
        """Get starting pose of a joint path file.

        Args:
            offset1: Path file name.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("GetPathStartPose({:s})".format(offset1))

    def set_safe_skin(self, offset1: int) -> str:
        """Configure safe-skin feature."""
        return self.send_recv_msg("SetSafeSkin({:d})".format(offset1))

    def set_obstacle_avoid(self, offset1: int) -> str:
        """Configure obstacle avoidance feature."""
        return self.send_recv_msg("SetObstacleAvoid({:d})".format(offset1))

    def set_collide_drag(self, offset1: int) -> str:
        """Configure collision drag mode.

        Args:
            offset1: Drag mode flag.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("SetCollideDrag({:d})".format(offset1))

    def start_drag(self) -> str:
        """Enable drag mode."""
        return self.send_recv_msg("StartDrag()")

    def stop_drag(self) -> str:
        """Disable drag mode."""
        return self.send_recv_msg("StopDrag()")

    def brake_control(self, offset1: int, offset2: int) -> str:
        """Control joint brakes.

        Args:
            offset1: Joint index.
            offset2: Brake control value.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("BrakeControl({:d},{:d})".format(offset1, offset2))

    def handle_traj_points(self, offset1: str) -> str:
        """Process a trajectory points file.

        Args:
            offset1: Trajectory file name.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("HandleTrajPoints({:s})".format(offset1))

    def tcp_speed(self, offset1: int) -> str:
        """Set TCP speed.

        Args:
            offset1: TCP speed value.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("TCPSpeed({:d})".format(offset1))

    def tcp_speed_end(self) -> str:
        """End TCP speed mode."""
        return self.send_recv_msg("TCPSpeedEnd()")

    def set_terminal_keys(self, offset1: int) -> str:
        """Configure terminal key behavior.

        Args:
            offset1: Key mode value.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg("SetTerminalKeys({:d})".format(offset1))

    def set_terminal_485(
        self, offset1: int, offset2: int, offset3: str, offset4: int
    ) -> str:
        """Set terminal RS-485 parameters.

        Args:
            offset1: Baud rate.
            offset2: Data bits.
            offset3: Parity setting.
            offset4: Stop bits.

        Returns:
            Robot response string.
        """
        return self.send_recv_msg(
            "SetTerminal485({:d},{:d},{:s},{:d})".format(
                offset1, offset2, offset3, offset4
            )
        )

    def get_terminal_485(self) -> str:
        """Get terminal RS-485 configuration."""
        return self.send_recv_msg("GetTerminal485()")
