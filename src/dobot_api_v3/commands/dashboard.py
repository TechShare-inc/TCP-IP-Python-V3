"""DobotApiDashboard — composed from command-category mixins.

The class is assembled via multiple inheritance:

    DobotApiDashboard
      ├── _SystemMixin   (lifecycle, script, motion-flow)
      ├── _IOMixin       (digital/analog I/O, Modbus)
      ├── _ConfigMixin   (speed, acc, jerk, coordinate, payload)
      ├── _QueryMixin    (queries, safety, drag, trajectory, terminal)
      └── DobotApi       (TCP socket base)

All protocol command implementations live in the four mixin files.
``DobotApiDashboard`` itself only provides the class docstring and re-exposes
the serialization helpers (``_fmt`` / ``_build_cmd``) that are already
inherited from :class:`~dobot_api_v3.commands._serialization._SerializationMixin`
through the mixin chain.
"""

from __future__ import annotations

from ..base import DobotApi
from ._config_mixin import _ConfigMixin
from ._io_mixin import _IOMixin
from ._query_mixin import _QueryMixin
from ._system_mixin import _SystemMixin


class DobotApiDashboard(_SystemMixin, _IOMixin, _ConfigMixin, _QueryMixin, DobotApi):
    """Dashboard command client for Dobot control APIs.

    This class sends robot lifecycle, I/O, configuration, and status commands
    over the dashboard TCP port (usually ``29999``).

    Commands are organized into four categories:

    * **System** — ``enable_robot``, ``disable_robot``, ``power_on``,
      ``emergency_stop``, ``speed_factor``, ``robot_mode``, script control,
      and queued-motion flow (``wait`` / ``pause`` / ``resume``).
    * **I/O** — digital output / input, analog output, DO groups, and Modbus.
    * **Config** — speed / acceleration / jerk ratios, coordinate selection,
      payload, and collision settings.
    * **Query** — pose / angle / error queries, kinematics solvers, safety
      configuration, drag mode, trajectory helpers, and terminal RS-485.

    The full source for each group lives in the corresponding private mixin
    module under ``dobot_api_v3/commands/``.
    """
