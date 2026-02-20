"""Error monitoring and recovery example.

See also:
- docs/reference/command-patterns.md#pattern-5-feedback--error-monitoring
- docs/reference/command-patterns.md#pattern-4-lifecycle--motion-ordering
"""

from dobot_api_v3 import DobotRobot


def main() -> None:
    """Read and clear current robot alarms."""
    with DobotRobot("192.168.5.1", language="en") as robot:
        has_errors = robot.check_errors(language="en")
        if not has_errors:
            print("No errors found.")
            return

        # robot.errors exposes the full RobotErrorMonitor API
        error_info = robot.errors.get_error_info(language="en")
        if error_info is not None:
            print(f"Error payload: {error_info}")

        robot.errors.save_error_log(language="en")
        is_cleared = robot.clear_and_recover(language="en")
        print(f"clear_and_recover result: {is_cleared}")


if __name__ == "__main__":
    main()
