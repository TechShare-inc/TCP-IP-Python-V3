"""Dobot API (modular V4-style architecture for V3 protocol semantics)."""

import os
import sys

from loguru import logger

from .base import PROTOCOL_FIELD_MAP, DobotApi, FeedbackDtype, MyType
from .dashboard import DobotApiDashboard
from .error_monitor import RobotErrorMonitor
from .feedback import DobotApiFeedBack, DobotApiFeedback
from .i18n_manager import AlarmI18n
from .move import DobotApiMove

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=os.environ.get("DOBOT_LOG_LEVEL", "INFO").upper(),
    colorize=True,
)

__version__ = "3.0.0"

__all__ = [
    # Primary names — use these in new code.
    "DobotApi",
    "DobotApiDashboard",
    "DobotApiMove",
    "DobotApiFeedback",
    "RobotErrorMonitor",
    "FeedbackDtype",
    "PROTOCOL_FIELD_MAP",
    "AlarmI18n",
    "logger",
    # Deprecated aliases — kept for backward compatibility.
    "DobotApiFeedBack",  # deprecated: use DobotApiFeedback
    "MyType",  # deprecated: use FeedbackDtype
]
