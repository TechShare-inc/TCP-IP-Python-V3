"""Dobot API - Python interface for TCP/IP communication with Dobot CR-V3 robots.

This package provides a clean, modular interface for controlling Dobot robotic arms
via TCP/IP protocol. It includes dashboard commands, motion commands, and real-time
feedback capabilities.

Example usage:
    from dobot_api import DobotApiDashboard, DobotApiMove, DobotApiFeedBack

    # Connect to robot
    dashboard = DobotApiDashboard("192.168.1.6", 29999)
    move = DobotApiMove("192.168.1.6", 30003)
    feedback = DobotApiFeedBack("192.168.1.6", 30004)

    # Enable robot
    dashboard.EnableRobot()

    # Move robot
    move.MovJ(0, 0, 0, 0, 0, 0)

    # Get feedback
    data = feedback.feedBackData()

    # Configure logging (optional)
    from dobot_api import configure_logging
    configure_logging(level="DEBUG")  # Enable debug output
"""

from loguru import logger

from dobot_api.alarms import (
    AlarmInfo,
    AlarmLevel,
    ControllerAlarms,
    ServoAlarms,
    get_alarm_info,
)
from dobot_api.alarms.lookup import alarmAlarmJsonFile
from dobot_api.base import DobotApi
from dobot_api.dashboard import DobotApiDashboard
from dobot_api.feedback import (
    DobotApiFeedBack,
    FeedbackType,
    MyType,  # Legacy alias
)
from dobot_api.move import DobotApiMove


def configure_logging(
    level: str = "INFO",
    format: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    sink=None,
) -> None:
    """Configure logging for the Dobot API.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format: Log message format string (loguru format)
        sink: Output sink (default: stderr). Can be a file path, file object, or callable.

    Example:
        # Enable debug logging to console
        configure_logging(level="DEBUG")

        # Log to file
        configure_logging(level="INFO", sink="dobot.log")

    """
    logger.remove()  # Remove default handler
    if sink is None:
        import sys

        sink = sys.stderr
    logger.add(sink, format=format, level=level, filter="dobot_api")


__version__ = "1.0.0"
__all__ = [
    # Core API classes
    "DobotApi",
    "DobotApiDashboard",
    "DobotApiMove",
    "DobotApiFeedBack",
    # Feedback data type
    "FeedbackType",
    "MyType",  # Legacy alias
    # Alarm system
    "AlarmInfo",
    "AlarmLevel",
    "ControllerAlarms",
    "ServoAlarms",
    "get_alarm_info",
    "alarmAlarmJsonFile",  # Legacy compatibility
    # Logging configuration
    "configure_logging",
]
