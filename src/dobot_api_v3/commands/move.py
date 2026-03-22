"""DobotApiMove — composed from move-command-category mixins."""

from __future__ import annotations

from ..base import DobotApi
from ._basic_motion_mixin import _BasicMotionMixin
from ._relative_motion_mixin import _RelativeMotionMixin
from ._servo_jog_mixin import _ServoJogMixin
from ._trajectory_mixin import _TrajectoryMixin


class DobotApiMove(
    _BasicMotionMixin,
    _RelativeMotionMixin,
    _ServoJogMixin,
    _TrajectoryMixin,
    DobotApi,
):
    """Movement command client for Dobot motion APIs.

    This class sends trajectory and servo commands to the move TCP port
    (usually ``30003``).

    Commands are organized into four categories:

    * **Basic motion** — ``mov_j``, ``mov_l``, ``joint_mov_j``, ``jump``,
      ``arc``, ``circle3``, ``mov_l_io``, ``mov_j_io``.
    * **Relative motion** — ``rel_mov_j``, ``rel_mov_l``,
      ``rel_mov_j_tool``, ``rel_mov_l_tool``, ``rel_mov_j_user``,
      ``rel_mov_l_user``, ``rel_joint_mov_j``.
    * **Servo & jog** — ``servo_j``, ``servo_js``, ``servo_p``,
      ``move_jog``.
    * **Trajectory** — ``start_trace``, ``start_path``, ``start_fc_trace``,
      ``sync``.
    """
