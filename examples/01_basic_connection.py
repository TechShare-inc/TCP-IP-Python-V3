"""Basic connection lifecycle example.

This script demonstrates how to connect to the dashboard port, enable the robot,
query basic status, and close the connection safely.

See also:
- docs/reference/command-patterns.md#pattern-1-positional-required-args
- docs/reference/command-patterns.md#pattern-4-lifecycle--motion-ordering
"""

from dobot_api_v3 import DobotApiDashboard


def main() -> None:
    """Run a basic connection sequence."""
    ip = "192.168.5.1"
    dashboard = DobotApiDashboard(ip, 29999)

    try:
        print("Clearing existing alarms...")
        print(dashboard.clear_error())

        print("Enabling robot...")
        print(dashboard.enable_robot())

        print("Robot mode:")
        print(dashboard.robot_mode())

        print("Current angle:")
        print(dashboard.get_angle())

        print("Current pose:")
        print(dashboard.get_pose())

        print("Disabling robot...")
        print(dashboard.disable_robot())
    finally:
        dashboard.close()


if __name__ == "__main__":
    main()
