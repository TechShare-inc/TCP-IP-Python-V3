"""Alarm lookup functions."""

from __future__ import annotations

from dobot_api.alarms.controller import ControllerAlarms
from dobot_api.alarms.models import AlarmInfo
from dobot_api.alarms.servo import ServoAlarms


def get_controller_alarm(alarm_id: int) -> AlarmInfo | None:
    """Look up a controller alarm by ID.

    Args:
        alarm_id: The alarm ID to look up

    Returns:
        AlarmInfo if found, None otherwise

    """
    return ControllerAlarms.get(alarm_id)


def get_servo_alarm(alarm_id: int) -> AlarmInfo | None:
    """Look up a servo alarm by ID.

    Args:
        alarm_id: The alarm ID to look up

    Returns:
        AlarmInfo if found, None otherwise

    """
    return ServoAlarms.get(alarm_id)


def get_alarm_info(alarm_id: int, alarm_type: str = "controller") -> AlarmInfo | None:
    """Look up an alarm by ID and type.

    Args:
        alarm_id: The alarm ID to look up
        alarm_type: Either "controller" or "servo"

    Returns:
        AlarmInfo if found, None otherwise

    """
    if alarm_type.lower() == "servo":
        return get_servo_alarm(alarm_id)
    return get_controller_alarm(alarm_id)


def get_all_alarms() -> tuple[dict, dict]:
    """Get all alarms as dictionaries (backward compatible with original JSON format).

    Returns:
        Tuple of (controller_alarms_dict, servo_alarms_dict)

    """
    controller_dict = {
        alarm_id: alarm.to_dict() for alarm_id, alarm in ControllerAlarms._alarms.items()
    }
    servo_dict = {alarm_id: alarm.to_dict() for alarm_id, alarm in ServoAlarms._alarms.items()}
    return controller_dict, servo_dict


# Legacy compatibility function
def alarmAlarmJsonFile():
    """Legacy function for backward compatibility.

    Returns:
        Tuple of (controller_alarms_list, servo_alarms_list)

    """
    controller_list = [alarm.to_dict() for alarm in ControllerAlarms._alarms.values()]
    servo_list = [alarm.to_dict() for alarm in ServoAlarms._alarms.values()]
    return controller_list, servo_list
