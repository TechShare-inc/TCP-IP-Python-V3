"""Unified Dobot TCP/IP API."""

from __future__ import annotations

from .dtypes import FeedbackData, Pose
from .error_monitor import RobotErrorMonitor
from .feedback import DobotApiFeedback
from .robot import DobotRobot

__version__ = "4.0.0a0"

__all__ = [
    "DobotRobot",
    "DobotApiFeedback",
    "FeedbackData",
    "Pose",
    "RobotErrorMonitor",
]
