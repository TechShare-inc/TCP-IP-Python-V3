"""Internal compatibility shim for modular Dobot API.

This module is intentionally non-primary. Use top-level imports from `dobot_api`.
"""

from .base import DobotApi, MyType
from .dashboard import DobotApiDashboard
from .feedback import DobotApiFeedBack
from .error_monitor import RobotErrorMonitor
from .i18n_manager import AlarmI18n

__all__ = [
    "DobotApi",
    "DobotApiDashboard",
    "DobotApiFeedBack",
    "RobotErrorMonitor",
    "AlarmI18n",
    "MyType",
]
