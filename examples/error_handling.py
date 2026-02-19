"""Error monitor demo using dashboard.get_error_id()."""

from dobot_api_v3 import RobotErrorMonitor
from dobot_api_v3.dashboard import DobotApiDashboard


def main() -> None:
    # Create a shared dashboard connection — pass it to RobotErrorMonitor so
    # that the same TCP socket can be reused by other API objects if needed.
    dashboard = DobotApiDashboard("192.168.5.1", 29999)
    monitor = RobotErrorMonitor(dashboard)

    try:
        # Get error information
        info = monitor.get_error_info(language="en")
        if info and info.get("errMsg"):
            print(f"Found {len(info['errMsg'])} errors:")
            for idx, error in enumerate(info["errMsg"], 1):
                print(
                    f"  {idx}. ID={error['id']}, Type={error['type']}, "
                    f"Level={error['level']}, Description={error['description']}"
                )

            # Clear errors
            print("\nClearing errors...")
            monitor.clear_robot_error(language="en")
        else:
            print("No errors found")

    finally:
        # The caller owns the dashboard — close it here.
        dashboard.close()


if __name__ == "__main__":
    main()
