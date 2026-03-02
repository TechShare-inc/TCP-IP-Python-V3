"""Motion parameter and coordinate configuration mixin for DobotApiDashboard."""

from __future__ import annotations

from ..utils import DynParam
from ._serialization import _SerializationMixin


class _ConfigMixin(_SerializationMixin):
    """Speed, acceleration, jerk, coordinate, and payload configuration commands."""

    def acc_j(self, speed: int) -> int:
        """Set joint acceleration ratio (MovJ / MovJIO / MovJR / JointMovJ).

        Args:
            speed: Joint acceleration ratio (1-100).

        Returns:
            Command queue ID.
        """
        return self._recv_ack("AccJ({:d})".format(speed))

    def acc_l(self, speed: int) -> int:
        """Set Cartesian acceleration ratio (MovL / MovLIO / MovLR / Jump / Arc / Circle).

        Args:
            speed: Cartesian acceleration ratio (1-100).

        Returns:
            Command queue ID.
        """
        return self._recv_ack("AccL({:d})".format(speed))

    def speed_j(self, speed: int) -> int:
        """Set joint speed ratio (MovJ / MovJIO / MovJR / JointMovJ).

        Args:
            speed: Joint speed ratio (1-100).

        Returns:
            Command queue ID.
        """
        return self._recv_ack("SpeedJ({:d})".format(speed))

    def speed_l(self, speed: int) -> int:
        """Set Cartesian speed ratio (MovL / MovLIO / MovLR / Jump / Arc / Circle).

        Args:
            speed: Cartesian speed ratio (1-100).

        Returns:
            Command queue ID.
        """
        return self._recv_ack("SpeedL({:d})".format(speed))

    def vel_j(self, speed: int) -> int:
        """Alias for :meth:`speed_j` (V4-style name)."""
        return self.speed_j(speed)

    def vel_l(self, speed: int) -> int:
        """Alias for :meth:`speed_l` (V4-style name)."""
        return self.speed_l(speed)

    def arch(self, index: int) -> int:
        """Set Jump gate parameter index (start lift height, max lift, end drop).

        Args:
            index: Jump parameter index (0-9).

        Returns:
            Command queue ID.
        """
        return self._recv_ack("Arch({:d})".format(index))

    def cp(self, ratio: int) -> int:
        """Set smooth transition ratio.

        Args:
            ratio: Smooth transition ratio (1-100).

        Returns:
            Command queue ID.
        """
        return self._recv_ack("CP({:d})".format(ratio))

    def lim_z(self, value: int) -> int:
        """Set maximum lifting height for door-type parameters.

        Args:
            value: Maximum lifting height.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("LimZ({:d})".format(value))

    def set_arm_orientation(self, r: int, d: int, n: int, cfg: int) -> int:
        """Set the hand command.

        Args:
            r: Forward/backward selector (1 for forward, -1 for backward).
            d: Elbow orientation (1 for up, -1 for down).
            n: Wrist flip selector (1 for no flip, -1 for flip).
            cfg: Sixth-axis angle configuration identifier.

        Returns:
            Command queue ID.
        """
        return self._recv_ack(
            "SetArmOrientation({:d},{:d},{:d},{:d})".format(r, d, n, cfg)
        )

    def payload(self, weight: float, inertia: float) -> int:
        """Set robot load.

        Args:
            weight: Payload weight.
            inertia: Payload moment of inertia.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("PayLoad({:f},{:f})".format(weight, inertia))

    def set_payload(self, offset1: float, *dyn_params: DynParam) -> int:
        """Set payload parameters.

        Args:
            offset1: Base payload value.
            *dyn_params: Additional payload arguments.

        Returns:
            Command queue ID.
        """
        string = "SetPayload({:f}".format(offset1)
        for params in dyn_params:
            string = string + str(params) + ","
        string = string + ")"
        return self._recv_ack(string)

    def set_collision_level(self, offset1: int) -> int:
        """Set collision detection level.

        Args:
            offset1: Collision level value.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("SetCollisionLevel({:d})".format(offset1))

    def set_user(self, index: int) -> int:
        """Select the calibrated user coordinate system.

        Args:
            index: Calibrated user coordinate index.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("User({:d})".format(index))

    def set_tool(self, index: int) -> int:
        """Select the calibrated tool coordinate system.

        Args:
            index: Calibrated tool coordinate index.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("Tool({:d})".format(index))

    def load_switch(self, offset1: int) -> int:
        """Switch load configuration.

        Args:
            offset1: Load profile index.

        Returns:
            Command queue ID.
        """
        return self._recv_ack("LoadSwitch({:d})".format(offset1))
