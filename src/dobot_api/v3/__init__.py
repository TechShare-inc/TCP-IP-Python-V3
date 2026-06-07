"""V3 protocol adapter exports."""

from __future__ import annotations

from dobot_api._vendor import ensure_vendor_paths

ensure_vendor_paths()

from dobot_api_v3.base import DobotApi  # noqa: E402
from dobot_api_v3.commands.dashboard import DobotApiDashboard  # noqa: E402
from dobot_api_v3.commands.move import DobotApiMove  # noqa: E402
from dobot_api_v3.dtypes import FeedbackData, FeedbackDtype  # noqa: E402
from dobot_api_v3.error_monitor import RobotErrorMonitor  # noqa: E402
from dobot_api_v3.feedback import DobotApiFeedback  # noqa: E402
from dobot_api_v3.i18n_manager import AlarmI18n  # noqa: E402

__all__ = [
    "DobotApi",
    "DobotApiDashboard",
    "DobotApiMove",
    "DobotApiFeedback",
    "FeedbackData",
    "FeedbackDtype",
    "RobotErrorMonitor",
    "AlarmI18n",
]
