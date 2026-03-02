"""Dobot API (modular V4-style architecture for V3 protocol semantics)."""

import os
import sys

from loguru import logger

from .base import PROTOCOL_FIELD_MAP, DobotApi, FeedbackData, FeedbackDtype
from .error_monitor import RobotErrorMonitor
from .feedback import DobotApiFeedback
from .i18n_manager import AlarmI18n
from .responses import (
    AckResponse,
    DobotApiError,
    ErrorIdResponse,
    IntResponse,
    PoseResponse,
    parse_response,
)
from .robot import DobotRobot

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
    "DobotRobot",
    "DobotApi",
    "DobotApiFeedback",
    "RobotErrorMonitor",
    "FeedbackData",
    "FeedbackDtype",
    "PROTOCOL_FIELD_MAP",
    "AlarmI18n",
    "logger",
    # Response types and parser.
    "DobotApiError",
    "AckResponse",
    "IntResponse",
    "PoseResponse",
    "ErrorIdResponse",
    "parse_response",
]
