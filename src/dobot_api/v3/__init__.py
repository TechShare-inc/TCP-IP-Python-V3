"""V3 protocol adapter exports.

Re-exports vendored V3 types through local submodules for clean
package structure matching the unified-wrapper design.
"""

from __future__ import annotations

from .commands.dashboard import DobotApiDashboard  # noqa: F401
from .commands.move import DobotApiMove  # noqa: F401
from .dtypes import FeedbackDtype  # noqa: F401

# Convenience re-exports for direct ``from dobot_api.v3 import ...`` usage
from dobot_api._vendor import ensure_vendor_paths

ensure_vendor_paths()

from dobot_api_v3.base import DobotApi  # noqa: E402
from dobot_api_v3.dtypes import FeedbackData  # noqa: E402
from dobot_api_v3.error_monitor import RobotErrorMonitor  # noqa: E402
from dobot_api_v3.feedback import DobotApiFeedback  # noqa: E402
from dobot_api_v3.i18n_manager import AlarmI18n  # noqa: E402

__all__ = [
    "DobotApi",
    "DobotApiDashboard",
    "DobotApiFeedback",
    "DobotApiMove",
    "FeedbackData",
    "FeedbackDtype",
    "RobotErrorMonitor",
    "AlarmI18n",
]
