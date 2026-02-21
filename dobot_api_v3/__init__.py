"""Dobot API (modular V4-style architecture for V3 protocol semantics)."""

import os
import sys
import warnings as _warnings

from loguru import logger

from .base import PROTOCOL_FIELD_MAP, DobotApi, FeedbackData, FeedbackDtype
from .dashboard import DobotApiDashboard
from .error_monitor import RobotErrorMonitor
from .feedback import DobotApiFeedback
from .i18n_manager import AlarmI18n
from .move import DobotApiMove
from .robot import DobotRobot

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=os.environ.get("DOBOT_LOG_LEVEL", "INFO").upper(),
    colorize=True,
)

__version__ = "3.0.0"

_DEPRECATED_NAMES: dict[str, object] = {
    "MyType": FeedbackDtype,
    "DobotApiFeedBack": DobotApiFeedback,
}

_DEPRECATED_MSG: dict[str, str] = {
    "MyType": "MyType is deprecated, use FeedbackDtype instead.",
    "DobotApiFeedBack": "DobotApiFeedBack is deprecated, use DobotApiFeedback instead.",
}


def __getattr__(name: str) -> object:
    """Emit DeprecationWarning for legacy package-level names (PEP 562)."""
    if name in _DEPRECATED_NAMES:
        _warnings.warn(_DEPRECATED_MSG[name], DeprecationWarning, stacklevel=2)
        return _DEPRECATED_NAMES[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    # Primary names — use these in new code.
    "DobotRobot",
    "DobotApi",
    "DobotApiDashboard",
    "DobotApiMove",
    "DobotApiFeedback",
    "RobotErrorMonitor",
    "FeedbackData",
    "FeedbackDtype",
    "PROTOCOL_FIELD_MAP",
    "AlarmI18n",
    "logger",
    # Deprecated aliases — kept for backward compatibility.
    "DobotApiFeedBack",  # deprecated: use DobotApiFeedback
    "MyType",  # deprecated: use FeedbackDtype
]
