"""V4 protocol adapter exports.

Re-exports vendored V4 types through local submodules for clean
package structure matching the unified-wrapper design.
"""

from __future__ import annotations

from .commands.dashboard import DobotApiDashboard  # noqa: F401
from .dtypes import FeedbackDtype  # noqa: F401
from .error_monitor import RobotErrorMonitor  # noqa: F401

# Convenience re-exports for direct ``from dobot_api.v4 import ...`` usage
from dobot_api._vendor import ensure_vendor_paths

ensure_vendor_paths()

from dobot_api_v4.feedback import DobotApiFeedback  # noqa: E402

__all__ = [
    "DobotApiDashboard",
    "DobotApiFeedback",
    "FeedbackDtype",
    "RobotErrorMonitor",
]
