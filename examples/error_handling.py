"""Error monitor demo using dashboard.GetErrorID()."""

from dobot_api_v3 import RobotErrorMonitor


def main() -> None:
    # Create monitor instance
    monitor = RobotErrorMonitor("192.168.5.1")

    # Connect to robot dashboard
    if not monitor.connect():
        print("Failed to connect to robot")
        return

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
        # Disconnect
        monitor.disconnect()


if __name__ == "__main__":
    main()
