"""Drag mode example using dashboard port.

This script demonstrates how to enable drag mode, allowing the user to manually
move the robot arm for a specified duration before disabling it.
"""

import time
from dobot_api_v3 import DobotApiDashboard


def main() -> None:
    """Run a drag mode sequence."""
    ip = "192.168.5.1"
    dashboard = DobotApiDashboard(ip, 29999)

    try:
        print("Clearing errors and enabling robot...")
        print(dashboard.clear_error())
        print(dashboard.power_on())
        time.sleep(10)  # Wait for the robot to power on
        print(dashboard.disable_robot())
        print(dashboard.enable_robot())

        # Set end effector 

        print("Starting drag mode. You can now move the robot manually.")
        print(dashboard.start_drag())

        # Allow the user to drag the robot for 10 seconds
        drag_duration = 10
        for i in range(drag_duration, 0, -1):
            print(f"Drag mode active for {i} more seconds...")
            time.sleep(1)

        print("Stopping drag mode.")
        print(dashboard.stop_drag())

        print("Disabling robot...")
        print(dashboard.disable_robot())
    finally:
        dashboard.close()


if __name__ == "__main__":
    main()
