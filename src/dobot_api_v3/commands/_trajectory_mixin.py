"""Trajectory replay and synchronization mixin for DobotApiMove."""

from __future__ import annotations

from ._serialization import _SerializationMixin


class _TrajectoryMixin(_SerializationMixin):
    """Trajectory file replay and command queue synchronization.

    Provides trajectory execution (Cartesian, joint, force-control) and
    the ``sync`` blocking primitive.
    """

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
