"""Basic connection lifecycle example.

This script demonstrates how to connect to the dashboard port, enable the robot,
query basic status, and close the connection safely.

See also:
- docs/reference/command-patterns.md#pattern-1-positional-required-args
- docs/reference/command-patterns.md#pattern-4-lifecycle--motion-ordering
"""

import time
from dobot_api_v3 import DobotApiDashboard


def main() -> None:
    """Run a basic connection sequence."""
    ip = "192.168.5.1"
    dashboard = DobotApiDashboard(ip, 29999)

    try:
        print("Clearing existing alarms...")
        print(dashboard.clear_error())

        time.sleep(1)  # Wait for the robot to clear alarms
        print("Enabling robot...")
        print(dashboard.enable_robot())

        time.sleep(1)  # Wait for the robot to enable
        print("Robot mode:")
        print(dashboard.robot_mode())

        time.sleep(1)  # Wait for the robot to update status
        print("Current angle:")
        print(dashboard.get_angle())

        time.sleep(1)  # Wait for the robot to update status
        print("Current pose:")
        print(dashboard.get_pose())

        time.sleep(1)  # Wait for the robot to update status
        print("Disabling robot...")
        print(dashboard.disable_robot())

    finally:
        time.sleep(1)  # Wait for the robot to disable
        dashboard.close()


if __name__ == "__main__":
    main()
