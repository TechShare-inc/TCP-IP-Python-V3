"""Basic connection lifecycle example.

This script demonstrates how to connect to the robot, run the standard startup
sequence, query basic status, and close all connections safely.

See also:
- docs/reference/command-patterns.md#pattern-1-positional-required-args
- docs/reference/command-patterns.md#pattern-4-lifecycle--motion-ordering
"""

from dobot_api_v3 import DobotRobot


def main() -> None:
    """Run a basic connection sequence."""
    ip = "192.168.5.1"

    with DobotRobot(ip, language="en") as robot:
        # startup() runs: clear_error -> power_on -> wait -> disable -> enable -> speed_factor
        robot.startup(speed=40)

        print("Robot mode:")
        print(robot.robot_mode())

        print("Current angle:")
        print(robot.get_angle())

        print("Current pose:")
        print(robot.get_pose())

        robot.shutdown()

    # All connections are closed automatically on exit from the ``with`` block.


if __name__ == "__main__":
    main()
