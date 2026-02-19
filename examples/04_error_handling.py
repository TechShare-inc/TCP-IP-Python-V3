"""Error monitoring and recovery example.

See also:
- docs/reference/command-patterns.md#pattern-5-feedback--error-monitoring
- docs/reference/command-patterns.md#pattern-4-lifecycle--motion-ordering
"""

from dobot_api_v3 import DobotApiDashboard, RobotErrorMonitor


def main() -> None:
    """Read and clear current robot alarms."""
    dashboard = DobotApiDashboard("192.168.5.1", 29999)
    monitor = RobotErrorMonitor(dashboard, language="en")

    try:
        has_errors = monitor.check_errors(language="en")
        if not has_errors:
            print("No errors found.")
            return

        error_info = monitor.get_error_info(language="en")
        if error_info is not None:
            print(f"Error payload: {error_info}")

        monitor.save_error_log(language="en")
        is_cleared = monitor.clear_robot_error(language="en")
        print(f"clear_robot_error result: {is_cleared}")
    finally:
        dashboard.close()


if __name__ == "__main__":
    main()
