"""Basic motion command mixin for DobotApiMove."""

from __future__ import annotations

from loguru import logger

from ..utils import DynParam
from ._serialization import _SerializationMixin


class _BasicMotionMixin(_SerializationMixin):
    """Basic absolute-target motion commands.

    Provides point-to-point, linear, arc, circle, and IO-coupled motion
    primitives.
    """

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
