"""Dobot API (modular V4-style architecture for V3 protocol semantics)."""

from .base import DobotApi, MyType
from .dashboard import DobotApiDashboard
from .move import DobotApiMove
from .feedback import DobotApiFeedBack
from .error_monitor import RobotErrorMonitor
from .i18n_manager import AlarmI18n

import os
import sys
from loguru import logger

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=os.environ.get("DOBOT_LOG_LEVEL", "INFO").upper(),
    colorize=True,
)

__version__ = "3.0.0"

__all__ = [
    "DobotApi",
    "DobotApiDashboard",
    "DobotApiMove",
    "DobotApiFeedBack",
    "RobotErrorMonitor",
    "MyType",
    "AlarmI18n",
    "logger",
]
