"""Internal compatibility shim for modular Dobot API.

This module is intentionally non-primary. Use top-level imports from `dobot_api`.
"""

from .base import DobotApi, FeedbackDtype, MyType, PROTOCOL_FIELD_MAP
from .dashboard import DobotApiDashboard
from .feedback import DobotApiFeedBack, DobotApiFeedback
from .error_monitor import RobotErrorMonitor
from .i18n_manager import AlarmI18n

__all__ = [
    # Primary names.
    "DobotApi",
    "DobotApiDashboard",
    "DobotApiFeedback",
    "RobotErrorMonitor",
    "AlarmI18n",
    "FeedbackDtype",
    "PROTOCOL_FIELD_MAP",
    # Deprecated aliases.
    "DobotApiFeedBack",  # deprecated: use DobotApiFeedback
    "MyType",  # deprecated: use FeedbackDtype
]
