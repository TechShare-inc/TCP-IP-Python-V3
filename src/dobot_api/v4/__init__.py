"""V4 protocol adapter exports."""

from __future__ import annotations

from dobot_api._vendor import ensure_vendor_paths

ensure_vendor_paths()

from dobot_api_v4.commands.dashboard import DobotApiDashboard  # noqa: E402
from dobot_api_v4.dtypes import FeedbackDtype  # noqa: E402
from dobot_api_v4.error_monitor import RobotErrorMonitor  # noqa: E402
from dobot_api_v4.feedback import DobotApiFeedback  # noqa: E402

__all__ = [
    "DobotApiDashboard",
    "DobotApiFeedback",
    "FeedbackDtype",
    "RobotErrorMonitor",
]
