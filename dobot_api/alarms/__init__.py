"""Alarm system for Dobot robots.

This module provides dataclasses for alarm information and lookup functions
to get alarm details by ID. Replaces the original JSON-based alarm system
with typed Python objects for better IDE support and type safety.
"""

from dobot_api.alarms.controller import ControllerAlarms
from dobot_api.alarms.lookup import get_alarm_info, get_controller_alarm, get_servo_alarm
from dobot_api.alarms.models import AlarmInfo, AlarmLevel, LocalizedText
from dobot_api.alarms.servo import ServoAlarms

__all__ = [
    # Data models
    "AlarmInfo",
    "AlarmLevel",
    "LocalizedText",
    # Alarm databases
    "ControllerAlarms",
    "ServoAlarms",
    # Lookup functions
    "get_alarm_info",
    "get_controller_alarm",
    "get_servo_alarm",
]
