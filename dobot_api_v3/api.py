"""Internal compatibility shim for modular Dobot API.

This module is intentionally non-primary. Use top-level imports from `dobot_api`.
"""

from .base import PROTOCOL_FIELD_MAP, DobotApi, FeedbackDtype, MyType
from .dashboard import DobotApiDashboard
from .error_monitor import RobotErrorMonitor
from .feedback import DobotApiFeedBack, DobotApiFeedback
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
