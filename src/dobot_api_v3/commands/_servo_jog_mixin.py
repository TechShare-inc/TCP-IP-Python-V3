"""Servo and jog command mixin for DobotApiMove."""

from __future__ import annotations

from ..utils import DynParam
from ._serialization import _SerializationMixin


class _ServoJogMixin(_SerializationMixin):
    """Real-time servo following and jog commands.

    Provides dynamic joint/Cartesian servo tracking and single-axis jog
    motion.
    """

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
